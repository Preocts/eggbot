""" Handle the consumption and processing of basic Channel commands

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    A basic channel command is any command that has a static, or list fed,
    response and replies back into the chat where executed.

    All commands can be permissioned by User, Channel, Role. All commands
    can be throttled with a Timeout setting in seconds.


"""
import logging
import json
import time
from . import json_io

logger = logging.getLogger(__name__)  # Create module level logger


class basicCommands:
    """ Defines the basicCommands class """

    def __init__(self, inputFile="./config/basicCommands.json"):
        """ Defines __init__ """
        logger.info(f'Initialize basicCommands: {inputFile}')
        self.bcConfig = {}
        self.activeConfig = None
        self.loadConfig(inputFile)
        return

    def __str__(self):
        return json.dumps(self.bcConfig, indent=4)

    def __bool__(self):
        if len(self.bcConfig):
            return True
        return False

    __nonzero__ = __bool__

    def commandCheck(self, guild: str, channel: str, user: str,
                     roles: list, message: str) -> dict:
        """ THINGS AND STUFF

            message is converted to lower case so all commands should be too!

            Args:

            Returns:

            Raises:
                I write the BEST DocStrings
        """

        cData = None
        cName = None
        # Do we have this guild?
        if not(guild in self.bcConfig.keys()):
            return {"status": False, "response": "Guild not configured"}

        # Is this user prohibited?
        if user in self.bcConfig[guild]["prohibitedUsers"]:
            return {"status": False, "response": "User Prohibited"}

        # Is this channel prohibited?
        if channel in self.bcConfig[guild]["prohibitedChannels"]:
            return {"status": False, "response": "Channel Prohibited"}

        # Is this a command?
        for t in self.bcConfig[guild]["guildCommands"]:
            if message.lower().startswith(t, 0, len(t)):
                cData = self.bcConfig[guild]["guildCommands"][t]
                cName = t
                break
        if cName is None:
            return {"status": False, "response": "No command found"}

        # Channel restrictions?
        if len(cData["channels"]) and not(channel in cData["channels"]):
            return {"status": False, "response": "Channel restricted"}

        # User restrictions?
        if len(cData["users"]) and not(user in cData["users"]):
            return {"status": False, "response": "User restricted"}

        # Role restrictions?
        if len(cData["roles"]) and not(roles in cData["roles"]):
            return {"status": False, "response": "Role restricted"}

        # Throttle restriction?
        if (time.time() - cData["lastran"]) < cData["throttle"]:
            return {"status": False, "response": "Throttle active"}

        self.bcConfig[guild]["guildCommands"][cName]["lastran"] = time.time()
        return {"status": True, "response": cData["content"]}

    def loadConfig(self, inputFile: str) -> bool:
        """ Load a config into the class

            Args:
                inputFile: JSON file to be loaded

            Returns:
                {"status": true/false, "response": str}

            Raises:
                None
        """

        try:
            self.bcConfig = json_io.loadConfig(inputFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {"status": False, "response": "Error loading config"}
        self.activeConfig = inputFile
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outputFile: str = None) -> bool:
        """ Save a config into the class

            Args:
                outputFile: JSON file to be loaded
                (If not provided, self.activeConfig is used)

            Returns:
                {"status": true/false, "response": str}

            Raises:
                None
        """

        if outputFile is None and self.activeConfig is None:
            logger.warning(f'saveConfig: No filename given to save')
            return {"status": False, "response": "Missing filename"}
        elif outputFile is None and len(self.activeConfig):
            outputFile = self.activeConfig
        try:
            self.bcConfig = json_io.saveConfig(self.bcConfig, outputFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        return {"status": True, "response": "Config saved"}
