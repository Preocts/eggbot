""" Handle the consumption and processing of basic Channel commands

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    A basic channel command is any command that has a static, or list fed,
    response and replies back into the chat where executed. Th
"""
import logging
import time
from . import json_io

logger = logging.getLogger(__name__)  # Create module level logger
GUILD_TEMPLATE = {"prohibitedChannels": [],
                  "prohibitedUsers": [],
                  "guildCommands": {}}
COMMAND_KEYS = ["users", "channels", "roles", "throttle",
                "lastran", "content", "help"]
COMMAND_DEFAULT = [[], [], [], 10, 0, "", ""]
COMMAND_DATATYPE = ["list", "list", "list", "int", "int", "str", "str"]


class basicCommands:
    """ Defines the basicCommands class """

    def __init__(self, inFile: str = "./config/basicCommands.json"):
        """ Defines __init__ """
        logger.info(f'Initialize basicCommands: {inFile}')
        self.bcConfig = {}
        self.activeConfig = None
        self.loadConfig(inFile)
        logger.info(f'Config loaded with {len(self.bcConfig)}')
        return

    def __str__(self):
        return str(self.bcConfig)

    def __bool__(self):
        if len(self.bcConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        if self.activeConfig is None:
            logger.warn('Lost activeConfig name while closing, not good.')
            logger.info('Dump file attempt: ./config/basicCommands_DUMP.json')
            self.activeConfig = "./config/basicCommands_DUMP.json"
        self.saveConfig(self.activeConfig)

    def commandCheck(self, guild: str, channel: str, roles: list,
                     user: str, message: str) -> dict:
        """ Scans a provided message for a command and return if found

            This function takes a list of args and scans the message provided
            for any matching commands in basicCommands.json (or active config).
            If found and allowed, the function passes just the content of the
            command back.

            Rules:
                All commands are not case sensitive. !test == !TEST

            Conditional checks. If any fail then return status = False
                In order:
                - Guild level checks:
                  - Is the guild listed in the config
                  - Is the channel listed as prohibited
                  - Is the user listed as prohibited
                  - Is there a matching command in the config
                - Command level checks:
                  - If defined, is this from an allowed ["channel"]
                  - If defined, is this from an allowoed ["user"]
                  - If defined, is this from an allowoed ["role"]
                  - If defined, is the command throttled
            If all of these pass you get Returns.

            Args:
                guild: Guild that the message came from
                channel: Channel name the message posted in
                roles: dicord.roles list of roles the user holds
                user: display_name of the message author (not nickname)
                message: The message to scan for a command.

            Returns:
                Pass:
                    {"status": True, "response": "command.content"}
                Fail:
                    {"status": False, "response": "[reason]"}

            Raises:
                None
        """
        logger.debug(f'{guild} | {channel} | {roles} | {user} | {message}')
        cData = None
        cName = None
        clean_roles = self.parseRoles(roles)
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
        if len(cData["roles"]) and not(clean_roles in cData["roles"]):
            return {"status": False, "response": "Role restricted"}

        # Throttle restriction?
        if (time.time() - cData["lastran"]) < cData["throttle"]:
            return {"status": False, "response": "Throttle active"}

        self.bcConfig[guild]["guildCommands"][cName]["lastran"] = time.time()
        logger.debug(f'Command returned: {cData["content"]}')
        return {"status": True, "response": cData["content"]}

    def addCommand(self, guild: str, input: str) -> dict:
        """ Add a command to the config unless it already exists """

        if not(len(input)):
            return {"status": False, "response": "No input"}
        logger.debug(f'addCommand: {guild} | {input}')
        sliceIn = input.split(" | ")
        trigger = sliceIn[0].split()[1]
        # capture input sans command and trigger
        content = " ".join(sliceIn.pop(0).split()[2:])
        # Check for empty content
        if (not(len(content)) and
           not(len(list(filter(lambda x: "content" in x, sliceIn))))):
            return {"status": False, "response": "No content to set"}
        # Check for guild config
        if not(guild in self.bcConfig.keys()):
            self.bcConfig[guild] = GUILD_TEMPLATE

        if trigger in self.bcConfig[guild]["guildCommands"].keys():
            logger.debug(f'Command exists: {trigger}')
            return {"status": False, "response": "Command exists"}

        self.bcConfig[guild]["guildCommands"][trigger] = {}
        for key in COMMAND_KEYS:
            keyValue = COMMAND_DEFAULT[COMMAND_KEYS.index(key)]
            self.bcConfig[guild]["guildCommands"][trigger][key] = keyValue

        if not(len(sliceIn)):
            # simple command
            logger.debug(f'Simple command: {trigger} | {content}')
            self.bcConfig[guild]["guildCommands"][trigger]["content"] = content
        else:
            # complex command
            logger.debug(f'Complex command: {trigger} | {sliceIn}')
            for o in sliceIn:
                if (not(len(o.split(" = ")))
                   and not(o.split(" = ") in COMMAND_KEYS)):
                    continue
                key = o.split(" = ")[0]
                value = o.split(" = ")[1]
                if COMMAND_DATATYPE[COMMAND_KEYS.index(key)] == "str":
                    self.bcConfig[guild]["guildCommands"][trigger][key] = value
                elif COMMAND_DATATYPE[COMMAND_KEYS.index(key)] == "int":
                    self.bcConfig[guild]["guildCommands"][trigger][key] = int(value)  # noqa: E501
                else:
                    self.bcConfig[guild]["guildCommands"][trigger][key].append(value)  # noqa: E501
        return {"status": True, "reponse": "Command set"}

    def loadConfig(self, inFile: str = "./config/basicCommands.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.bcConfig = json_io.loadConfig(inFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {"status": False, "response": "Error loading config"}
        self.activeConfig = inFile
        logger.debug(f'loadConfig success: {inFile}')
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/basicCommands.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            json_io.saveConfig(self.bcConfig, outFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'saveConfig success: {outFile}')
        return {"status": True, "response": "Config saved"}

    def parseRoles(self, discord_roles):
        """ Creates a easier to read list of user roles.

            Discord Format:
                [<Role id=621085335979294740 name='@everyone'>,
                 <Role id=662091435813765130 name='Egg Tester'>,
                 <Role id=649721426789662739 name='Owner'>]

            What we want:
                ['@everyone', 'Egg Tester', 'Owner']
        """

        clean_roles = []
        for r in discord_roles:
            clean_roles.append(r.name)
        logging.debug(f'parseRoles: {clean_roles}')
        return clean_roles

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
