"""
    joinActions is a module for Egg_Bot for welcome messages

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    Someone joins the guild, we might want to:
        - Assign a role to this lovely person
        - Check to see if this invite is tied to a specific role
          - Assign that role
        - Find active DM messages to send (by role)
          - Send them
        - Find active Chat messages to post (by role)
          - Post them

    So from the config we need an invite join table, welcome message,
    default role assignments, channel name, and active toggle
    We also want to set a welcome message, default role, invite roles,
    and toggle messages
"""
import logging
from . import json_io

logger = logging.getLogger(__name__)  # Create module level logger


class joinActions:
    """ Defines the joinActions class """

    def __init__(self, inFile: str = "./config/joinActions.json"):
        """ Define __init__ """
        logger.info(f'Initialize joinActions: {inFile}')
        self.jaConfig = {}
        self.activeConfig = ''
        self.loadConfig(inFile)
        logger.info(f'Config loaded with {len(self.jaConfig)}')
        return

    def __str__(self):
        return str(self.jaConfig)

    def __bool__(self):
        if len(self.jaConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        if self.activeConfig is None:
            logger.warn('Lost activeConfig name while closing, not good.')
            logger.info('Dump file attempt: ./config/joinActions_DUMP.json')
            self.activeConfig = "./config/joinActions_DUMP.json"
        self.saveConfig(self.activeConfig)

    def create(self, guild: str, **kwargs) -> dict:
        """
        Creates a new join action in the configuration file

        Keyword arguements are optional, the config entry will be populated
        with empty values. .update() can be used to edit. Returns a failure
        if the "name" keyword already exists in the configuration file.

        Args:
            guild (int): discord.guild.id

        **kwargs:
            name (str): Unique name for the join action
            channel (str): Channel ID any message is displayed.
                           Leaving this blank will result in a direct message
            message (str): Displays this message to given channel/DM
            active (bool): Controls if the action is used or not

        Not currently used:
            addRole (str): Grants user a list of roles IDs on join
            limitRole (str): List roles IDs to recieve this join action
            limitInvite (str): List invite IDs to recieve this join action

        Returns:
            (dict) : {"status": true/false, "response": str}

        Raises:
            None
        """

        logger.debug(f'create: {guild} | {kwargs.items()}')
        try:
            guild = str(guild)
        except ValueError as err:
            return {"status": False, "response": err}
        # Default Config, change to add/remove:
        config = {'name': '',
                  'channel': '',
                  'roles': '',
                  'message': '',
                  'active': True,
                  'limitRole': '',
                  'limitInvite': ''}
        for key, value in kwargs.items():
            if key in config:
                config[key] = value
        if len(config["name"]) == 0:
            logger.debug('Name not provided for join action')
            return {"status": False, "response": "Name not defined"}
        if not(guild in self.jaConfig):
            self.jaConfig[guild] = [config, ]
        else:
            for n in self.jaConfig[guild]:
                if n["name"] == config["name"]:
                    logger.info(f'Name already exists: {config["name"]}')
                    return {"status": False, "response": "Name already exists"}
            self.jaConfig[guild].append(config)
        logger.debug(f'Join action added for {guild} | {config}')
        return {"status": True, "response": "Join action created"}

    def read(self, guild: str, name: str) -> dict:
        """
        Return a specific action for a guild

        Args:
            guild (str): ID of the guild
            name (str): Name of the join action being requested

        Returns:
            (dict) : {"status": true/false, "response": str}

        Raises:
            None
        """

        logger.debug(f'read: {guild} | {name}')
        if not(guild in self.jaConfig):
            logger.debug('Read: Guild not found')
            return {"status": False, "response": "Guild not found"}
        for n in self.jaConfig[guild]:
            if n["name"] == name:
                logger.debug('Read: Join action found')
                return {"status": True, "response": n}
        logger.debug('Read: Name not found')
        return {"status": False, "response": "Name not found"}

    def readAll(self, guild: str) -> dict:
        """
        Return all actions for a guild

        Args:
            guild (str): ID of the guild

        Returns:
            (dict) : {"status": true/false, "response": list}

        Raises:
            None
        """

        logger.debug(f'readAll: {guild}')
        if not(guild in self.jaConfig):
            logger.debug('readAll: Guild not found')
            return {"status": False, "response": "Guild not found"}
        return{"status": True, "response": self.jaConfig[guild]}

    def update(self, guild: str, name: str, **kwargs) -> dict:
        """
        Update an existing join action in the configuration file

        Keyword arguements are optional, the config entry will be populated
        with current values. Return a failure if the name keyword is not found.
        This cannot and will not rename a join action. "name" is ignored in
        the keywords.

        Args:
            guild (str): ID of the guild
            name (str): Name of the join action being updated
        **kwargs:
            See .create()

        Returns:
            (dict) : {"status": true/false, "response": str}

        Raises:
            None
        """

        logger.debug(f'Update: {guild} | {name} | {kwargs.items()}')
        results = self.read(guild, name)
        if not(results["status"]):
            return {"status": False, "response": "Guild or Name not found"}
        config = results["response"]
        for key, value in kwargs.items():
            if (key in config) and (key != 'name'):
                config[key] = value

        for action in self.jaConfig[guild]:
            if action["name"] == name:
                i = self.jaConfig[guild].index(action)
                logger.debug(f'Update: Updating join action index: {i}')
                self.jaConfig[guild][i] = config
                return {"status": True, "response": "Join action updated"}
        logger.warning(f'Something went wrong: name missing')
        return {"status": False, "response": "Something went wrong"}

    def delete(self, guild: str, name: str) -> dict:
        """
        Deletes a stored config for welcome messages

        Args:
            guild (str): ID of the guild
            name (str): Name of the join action being requested

        Returns:
            (dict) : {"status": true/false, "response": str}

        Raises:
            None
        """
        logger.debug(f'deleteMessage: {guild} | {name}')
        if not(guild in self.jaConfig):
            logger.debug('Delete: Guild not found')
            return {"status": False, "response": "Guild not found"}
        for n in self.jaConfig[guild]:
            if n["name"] == name:
                logger.debug(f'Deleting join action name: {name}')
                i = self.jaConfig[guild].index(n)
                del self.jaConfig[guild][i]
                return {"status": True, "response": "Join action deleted"}
        logger.debug('Delete: Name not found')
        return {"status": False, "response": "Join action name not found"}

    def loadConfig(self, inFile: str = "./config/joinActions.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.jaConfig = json_io.loadConfig(inFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {"status": False, "response": "Error loading config"}
        self.activeConfig = inFile
        logger.debug(f'loadConfig success: {inFile}')
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/joinActions.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            json_io.saveConfig(self.jaConfig, outFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'loadConfig success: {outFile}')
        return {"status": True, "response": "Config saved"}

    def getJoinMessage(self, guild: str, user: str) -> dict:
        """
        Returns any join messages to send

        Args:
            guild (str): ID of the guild
            user (str): ID of the user that joined

            Returns:
                (dict) :
                    {"status": True,
                     "response":
                        [{"message": "Message to send",
                         "channel": int},]
                    }
                    If status is fales, response contains reason why
                    If channel is blank, the message is intended to be a DM

            Raises:
                None
        """

        joinMessages = []
        results = self.readAll(guild)
        if not(results["status"]):
            logger.debug(f'Guild not configured: {guild}')
            return {"status": False, "response": "Guild not configured"}
        actions = results["response"]
        logger.debug(f'joinActions found: {actions}')

        for a in actions:
            if a["active"]:
                try:
                    joinMessages.append({"message": a["message"],
                                        "channel": int(a["channel"])})
                except ValueError as err:
                    logger.warning(f"Bad join action: {guild} | {a} | {err}")
                    continue
        if not(len(joinMessages)):
            logger.debug('No active join actions found')
            return {"status": False, "response": "No join actions found"}
        logger.debug(f'Join actions: {joinMessages}')
        return {"status": True, "response": joinMessages}

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
