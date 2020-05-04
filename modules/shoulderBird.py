"""
    ShoulderBird is a Discord channel alert tool

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
        results = SB.putBird("guild", "user", "RegEx Search String")

    Add/Remove ignore name:
        results = SB.gagBird("guild", "user")

    Delete a search:
        results = SB.delBird("guild", "user")

    Toggle a search on/off (returns new state):
        results = SB.toggleBird("guild", "user")

    Scan a message for a matching search:
        results = SB.birdCall("guild", "user", "Message String")
        # If results["status"] is True then results["response"] will be
        # the user of who had a matching search.

    Save Config:
        SB.saveConfig("FileNameOptional")
"""
import logging
import re
from . import json_io

logger = logging.getLogger(__name__)  # Create module level logger


class shoulderBird:
    """
    Defines the ShouldBird Object

    Config format:
    {
        "guild" {
            "user": {
                "regex": "Expression",
                "toggle": Boolean,
                "ignore": ["string",]
            }
        }
    }

    Definitions:
        Bird : A single search string in regEx
    """

    def __init__(self, inFile: str = "./config/shoulderBird.json"):
        """INIT"""
        logging.info(f'Start: Initializing shoulderBird: {inFile}')
        self.sbConfig = {}
        self.activeConfig = ""
        self.loadConfig(inFile)
        logger.info(f'Config loaded with {len(self.sbConfig)}')
        return

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
            logger.info('Dump file attempt: ./config/shoulderBird_DUMP.json')
            self.activeConfig = "./config/shoulderBird_DUMP.json"
        self.saveConfig(self.activeConfig)

    def getBirds(self, guild: str) -> dict:
        """
        Fetch all defined Birds from the config file

        Args:
            guild (str): Guild ID to pull results from

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'getBirds: {guild}')
        if ((guild in self.sbConfig) and
           len(self.sbConfig[guild])):
            return {"status": True, "response": self.sbConfig[guild]}
        return {"status": False, "response": "Guild not found or empty"}

    def getBird(self, guild: str, user: str) -> dict:
        """
        Fetch a single defined Bird from the config file

        Args:
            guild (str): Guild ID to pull results from
            user (str): User ID to pull results for

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'getBird call: {guild} | {user}')
        if ((guild in self.sbConfig) and
           len(self.sbConfig[guild])):
            if user in self.sbConfig[guild]:
                if self.sbConfig[guild][user]["toggle"]:
                    response = self.sbConfig[guild][user]["regex"]
                    return {"status": True, "response": response}
                else:
                    return {"status": False, "response": "Toggled off"}
        return {"status": False, "response": "Guild or user not found"}

    def putBird(self, guild: str, user: str, regex: str) -> dict:
        """
        Stores a Bird into the loaded config

        Args:
            guild (str): Guild ID to assign
            user (str): User ID to assign
            regex (str): Regex expression to search chat with
                         All expressions are word-bound be default and
                         case insensitive

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'putBird: {guild} | {user} | {regex}')
        if not(guild in self.sbConfig):
            self.sbConfig[guild] = {}
        self.sbConfig[guild][user] = {}
        self.sbConfig[guild][user]["regex"] = regex
        self.sbConfig[guild][user]["toggle"] = False
        self.sbConfig[guild][user]["ignore"] = []
        return {"status": True, "response": "Bird put in config"}

    def delBird(self, guild: str, user: str) -> dict:
        """
        Removes a Bird from the loaded config

        Args:
            guild (str): Guild ID
            user (str): User ID to delete

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'delBirds: {guild} | {user}')
        if guild in self.sbConfig:
            if user in self.sbConfig[guild]:
                del self.sbConfig[guild][user]
                return {"status": True, "response": "Bird deleted"}
        return {"status": False, "response": "Guild or user not found"}

    def toggleBird(self, guild: str, user: str) -> dict:
        """
        Toggles ShoulderBird for a specific guild

        Args:
            guild (str): Guild ID
            user (str): User ID to toggle

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'delBirds: {guild} | {user}')
        if guild in self.sbConfig:
            if user in self.sbConfig[guild]:
                curToggle = self.sbConfig[guild][user]["toggle"]
                if curToggle:
                    curToggle = False
                else:
                    curToggle = True
                self.sbConfig[guild][user]["toggle"] = curToggle
        return {"status": curToggle, "response": None}

    def birdCall(self, guild: str, user: str, message: str) -> dict:
        """
        Uses regEx to find defined keywords in a chat message

        Args:
            guild (str): Guild ID to pull results from
            user (str): User ID to pull results for
            message (str): Message content to run regex against

        Returns:
            (dict) : {"status": bool, "response": (list)[UserIDs]}

        Raises:
            None
        """

        logger.debug(f'Bird Call: {guild} | {user} | {message}')
        # Is the guild configured?
        results = self.getBirds(guild)
        if not(results["status"]):
            logger.debug(f'Guild returned no results: {guild}')
            return {"status": False, "Response": []}
        nest = results["response"]
        birdList = []
        for bird in nest:
            # check all available active regex for a hit
            if nest[bird]["toggle"]:
                if user in nest[bird]["ignore"]:
                    continue
                rx = nest[bird]["regex"]
                findRg = re.compile(r'\b{}\b'.format(rx), re.I)
                found = findRg.search(message)
                if found:
                    logger.info(f'Bird found for {bird}')
                    try:
                        birdList.append(int(bird))
                    except ValueError as e:
                        logger.warning(f'Bad bird: {guild} | {user} | {e}')
                        continue
        if len(birdList):
            return {"status": True, "response": birdList}
        logger.info('Empty Nest')
        return {"status": False, "repsonse": []}

    def gagBird(self, guild: str, user: str, target: str) -> dict:
        """
        Toggles a given target for a given guild to be ignored

        While logging messages may capture messages from ignored users if
        the logging levels are set low enough, ignored users will not trigger
        a shoulderBird alert.

        Hopefully, someday, Discord figures out the simple application of
        display: none; to hide blocked users in the channel history. >:V

        Args:
            guild (str): Guild ID
            user (str): User ID to assign config to
            target (str): User ID to ignore

        Returns:
            {"status": True/False, "response": "string"}

        Raises:
            None
        """

        logger.debug(f'Gag Bird: {guild} | {user}')
        if not(guild in self.sbConfig):
            return {"status": False, "response": "No nests in that guild"}
        if not(user in self.sbConfig[guild]):
            return {"status": False, "response": "No bird by that user"}
        if target in self.sbConfig[guild][user]["ignore"]:
            ix = self.sbConfig[guild][user]["ignore"].index(target)
            self.sbConfig[guild][user]["ignore"].pop(ix)
            logger.debug(f'Bird listening: {target}')
            return {"status": True,
                    "response": f"ShoulderBird listen to {target} now"}
        else:
            self.sbConfig[guild][user]["ignore"].append(target)
            logger.dubug(f'Bird ignoring: {target}')
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
        logger.debug(f'loadConfig success: {inFile}')
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/shoulderBird.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            json_io.saveConfig(self.sbConfig, outFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'saveConfig success: {outFile}')
        return {"status": True, "response": "Config saved"}

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
