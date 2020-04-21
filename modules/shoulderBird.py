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
                    "toggle": Boolean
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
        self.shoulderBird = {}
        self.activeConfig = ""
        self.loadConfig(inFile)
        return None

    def __str__(self):
        return str(self.shoulderBird)

    def __bool__(self):
        if len(self.shoulderBird):
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
        if ((guildname in self.shoulderBird) and
           len(self.shoulderBird[guildname])):
            return {"status": True, "response": self.shoulderBird[guildname]}
        return {"status": False, "response": "Guild not found or empty"}

    def getBird(self, guildname: str, username: str) -> dict:
        """ Fetch a single defined Bird from the config file """

        logger.debug(f'getBird call: {guildname} | {username}')
        if ((guildname in self.shoulderBird) and
           len(self.shoulderBird[guildname])):
            if username in self.shoulderBird[guildname]:
                if self.shoulderBird[guildname][username]["toggle"]:
                    response = self.shoulderBird[guildname][username]["regex"]
                    return {"status": True, "response": response}
                else:
                    return {"status": False, "response": "Toggled off"}
        return {"status": False, "response": "Guild or user not found"}

    def putBird(self, guildname: str, username: str, regex: str) -> dict:
        """ Stores a Bird into the loaded config """

        logger.debug(f'putBird: {guildname} | {username} | {regex}')
        if not(guildname in self.shoulderBird):
            self.shoulderBird[guildname] = {}
        self.shoulderBird[guildname][username] = {}
        self.shoulderBird[guildname][username]["regex"] = regex
        self.shoulderBird[guildname][username]["toggle"] = False
        return {"status": True, "response": "Bird put in config"}

    def delBird(self, guildname: str, username: str) -> dict:
        """ Removes a Bird from the loaded config """

        logger.debug(f'delBirds: {guildname} | {username}')
        if guildname in self.shoulderBird:
            if username in self.shoulderBird[guildname]:
                del self.shoulderBird[guildname][username]
                return {"status": True, "response": "Bird deleted"}
        return {"status": False, "response": "Guild or user not found"}

    def toggleBird(self, guildname: str, username: str) -> dict:
        """ Toggles ShoulderBird for a specific guild """

        logger.debug(f'delBirds: {guildname} | {username}')
        if guildname in self.shoulderBird:
            if username in self.shoulderBird[guildname]:
                curToggle = self.shoulderBird[guildname][username]["toggle"]
                if curToggle:
                    curToggle = False
                else:
                    curToggle = True
                self.shoulderBird[guildname][username]["toggle"] = curToggle
        return {"status": curToggle, "response": None}

    def birdCall(self, guildname: str, username: str, message: str) -> dict:
        """ Uses regEx to find defined keywords in a chat message

        Args:
            sMessage: The message being scanned (use message.clean_content)
            sSearch: The regEx string of the Bird

        Returns:

        """

        logger.info(f'Bird Call: {guildname} | {username} | {message}')
        results = self.getBirds(guildname)
        if not(results["status"]):
            return {"status": False, "Response": None}
        nest = results["response"]
        for bird in nest:
            if bird == username and nest[bird]["toggle"]:
                rx = nest[bird]["regex"]
                findRg = re.compile(r'\b{}\b'.format(rx), re.I)
                found = findRg.search(message)
                if found:
                    logger.info(f'Bird found for {bird}')
                    return {"status": True, "response": bird}
        logger.info('Empty Nest')
        return {"status": False, "repsonse": None}

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
            self.sbConfig = json_io.saveConfig(self.sbConfig, outFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        return {"status": True, "response": "Config saved"}

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
