""" ShoulderBird is a Discord channel alert tool

    Alerts a user when a keyword of their choice is said in any chat
    that is being watched by the bot.

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    Common Use Examples:
    ---
    Initialize: (loads config)
        SB = shoulderBird.shoulderBird("FileNameOptional")

    Create/Update a search:
        results = SB.putBird("GuildName", "UserName", "RegEx Search String")

    Add/Remove ignore name:
        results = SB.gagBird("GuildName", "UserName")

    Delete a search:
        results = SB.delBird("GuildName", "UserName")

    Toggle a search on/off (returns new state):
        results = SB.toggleBird("GuildName", "UserName")

    Scan a message for a matching search:
        results = SB.birdCall("GuildName", "UserName", "Message String")
        # If results["status"] is True then results["response"] will be
        # the username of who had a matching search.

    Save Config:
        SB.saveConfig("FileNameOptional")
"""
import logging
import re
from . import json_io

logger = logging.getLogger(__name__)  # Create module level logger


class shoulderBird:
    """Defines the ShouldBird Object

        Config format:
        {
            "guildname" {
                "username": {
                    "regex": "Expression",
                    "toggle": Boolean,
                    "ignore": ["string",]
                }
            }
        }

        Definitions:
            Bird : A single search string in regEx

        Returns:
            {
                "status": True/False,
                "response": [output]
            }
    """

    def __init__(self, inFile: str = "./config/shoulderBird.json"):
        """INIT"""
        logging.info(f'Start: Initializing shoulderBird: {inFile}')
        self.sbConfig = {}
        self.activeConfig = ""
        self.loadConfig(inFile)
        return None

    def __str__(self):
        return str(self.sbConfig)

    def __bool__(self):
        if len(self.sbConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        if self.activeConfig is None:
            logger.warn('Lost activeConfig name while closing, not good.')
            self.activeConfig = "./config/shoulderBird_DUMP.json"
        self.saveConfig(self.activeConfig)

    def getBirds(self, guildname: str) -> dict:
        """ Fetch all defined Birds from the config file """

        logger.debug(f'getBirds: {guildname}')
        if ((guildname in self.sbConfig) and
           len(self.sbConfig[guildname])):
            return {"status": True, "response": self.sbConfig[guildname]}
        return {"status": False, "response": "Guild not found or empty"}

    def getBird(self, guildname: str, username: str) -> dict:
        """ Fetch a single defined Bird from the config file """

        logger.debug(f'getBird call: {guildname} | {username}')
        if ((guildname in self.sbConfig) and
           len(self.sbConfig[guildname])):
            if username in self.sbConfig[guildname]:
                if self.sbConfig[guildname][username]["toggle"]:
                    response = self.sbConfig[guildname][username]["regex"]
                    return {"status": True, "response": response}
                else:
                    return {"status": False, "response": "Toggled off"}
        return {"status": False, "response": "Guild or user not found"}

    def putBird(self, guildname: str, username: str, regex: str) -> dict:
        """ Stores a Bird into the loaded config """

        logger.debug(f'putBird: {guildname} | {username} | {regex}')
        if not(guildname in self.sbConfig):
            self.sbConfig[guildname] = {}
        self.sbConfig[guildname][username] = {}
        self.sbConfig[guildname][username]["regex"] = regex
        self.sbConfig[guildname][username]["toggle"] = False
        self.sbConfig[guildname][username]["ignore"] = []
        return {"status": True, "response": "Bird put in config"}

    def delBird(self, guildname: str, username: str) -> dict:
        """ Removes a Bird from the loaded config """

        logger.debug(f'delBirds: {guildname} | {username}')
        if guildname in self.sbConfig:
            if username in self.sbConfig[guildname]:
                del self.sbConfig[guildname][username]
                return {"status": True, "response": "Bird deleted"}
        return {"status": False, "response": "Guild or user not found"}

    def toggleBird(self, guildname: str, username: str) -> dict:
        """ Toggles ShoulderBird for a specific guild """

        logger.debug(f'delBirds: {guildname} | {username}')
        if guildname in self.sbConfig:
            if username in self.sbConfig[guildname]:
                curToggle = self.sbConfig[guildname][username]["toggle"]
                if curToggle:
                    curToggle = False
                else:
                    curToggle = True
                self.sbConfig[guildname][username]["toggle"] = curToggle
        return {"status": curToggle, "response": None}

    def birdCall(self, guildname: str, username: str, message: str) -> dict:
        """ Uses regEx to find defined keywords in a chat message

        Args:
            sMessage: The message being scanned (use message.clean_content)
            sSearch: The regEx string of the Bird

        Returns:
            {"status": true, "response": ["usernames"]}

        Raises:
            None
        """

        logger.debug(f'Bird Call: {guildname} | {username} | {message}')
        # Is the guild configured?
        results = self.getBirds(guildname)
        if not(results["status"]):
            logger.debug(f'Guild returned no results: {guildname}')
            return {"status": False, "Response": None}
        nest = results["response"]
        birdList = []
        for bird in nest:
            # check all available active regex for a hit
            if nest[bird]["toggle"]:
                rx = nest[bird]["regex"]
                findRg = re.compile(r'\b{}\b'.format(rx), re.I)
                found = findRg.search(message)
                if found:
                    logger.info(f'Bird found for {bird}')
                    birdList.append(bird)
        if len(birdList):
            return {"status": True, "response": birdList}
        logger.info('Empty Nest')
        return {"status": False, "repsonse": []}

    def gagBird(self, guildname: str, username: str, target: str) -> dict:
        """ Toggles a given target for a given guild to be ignored

        While logging messages may capture messages from ignored users if
        the logging levels are set low enough, ignored users will not trigger
        a shoulderBird alert.

        Hopefully, someday, Discord figures out the simple application of
        display: none; to hide blocked users in the channel history. >:V

        Args:
            guildname: Name of the guild to configure
            username: Username of ShoulderBird user
            target: Username (not nickname) of user to ignore

        Returns:
            {"status": True/False, "response": "string"}

        Raises:
            None
        """

        logger.debug(f'Gag Bird: {guildname} | {username}')
        if not(guildname in self.sbConfig):
            return {"status": False, "response": "No nests in that guild"}
        if not(username in self.sbConfig[guildname]):
            return {"status": False, "response": "No bird by that username"}
        if target in self.sbConfig[guildname][username]["ignore"]:
            ix = self.sbConfig[guildname][username]["ignore"].index(target)
            self.sbConfig[guildname][username]["ignore"].pop(ix)
            return {"status": True,
                    "response": f"ShoulderBird listen to {target} now"}
        else:
            self.sbConfig[guildname][username]["ignore"].append(target)
            return {"status": True,
                    "response": f"ShoulderBird ignore {target} now"}

    def loadConfig(self, inFile: str = "./config/shoulderBird.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.sbConfig = json_io.loadConfig(inFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {"status": False, "response": "Error loading config"}
        self.activeConfig = inFile
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/shoulderBird.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            json_io.saveConfig(self.sbConfig, outFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        return {"status": True, "response": "Config saved"}

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
