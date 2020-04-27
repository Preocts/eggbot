""" joinActions is a module for Egg_Bot for welcome messages

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
            self.activeConfig = "./config/joinActions_DUMP.json"
        self.saveConfig(self.activeConfig)

    def create(self, guildname: str, **kwargs) -> dict:
        """ Creates a new join action in the configuration file

        Keyword arguements are optional, the config entry will be populated
        with empty values. .update() can be used to edit. Returns a failure
        if the "name" keyword already exists in the configuration file.

        Args:
            guildname: Target guildname
            [name], (optionals set by config)

        Keys:
            name: Unique name for the join action
            channel: Channel any message is displayed.
                     Leaving this blank will result in a direct message
            addRole: Grants user a list of roles on join
            message: Displays this message to given channel/DM
            active: Boolean toggle

            limitRole: List roles required to recieve this join action
            limitInvite: List invite IDs required to recieve this join action

        Returns:
            {"status": true/false, "response": str}
        """

        logger.debug(f'create: {guildname} | {kwargs.items()}')
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
            logger.info('Name not provided for join action')
            return {"status": False, "response": "Name not defined"}
        if not(guildname in self.jaConfig):
            self.jaConfig[guildname] = [config, ]
        else:
            for n in self.jaConfig[guildname]:
                if n["name"] == config["name"]:
                    logger.info(f'Name already exists: {config["name"]}')
                    return {"status": False, "response": "Name already exists"}
            self.jaConfig[guildname].append(config)
        logger.info(f'Join action added for {guildname}')
        return {"status": True, "response": "Join action created"}

    def read(self, guildname: str, name: str) -> dict:
        """ Return a specific action for a guild

            Returns:
                {"status": true/false, "response": str}
        """

        logger.debug(f'read: {guildname} | {name}')
        if not(guildname in self.jaConfig):
            logger.info('Guild not found')
            return {"status": False, "response": "Guild not found"}
        for n in self.jaConfig[guildname]:
            if n["name"] == name:
                logger.info('Join action found')
                return {"status": True, "response": n}
        logger.info('Name not found')
        return {"status": False, "response": "Name not found"}

    def readAll(self, guildname: str) -> dict:
        """ Return all actions for a guild

            Returns:
                {"status": true/false, "response": str}
        """

        logger.debug(f'readAll: {guildname}')
        if not(guildname in self.jaConfig):
            logger.info('Guild not found')
            return {"status": False, "response": "Guild not found"}
        return{"status": True, "response": self.jaConfig[guildname]}

    def update(self, guildname: str, name: str, **kwargs) -> dict:
        """ Update an existing join action in the configuration file

        Keyword arguements are optional, the config entry will be populated
        with current values. Return a failure if the name keyword is not found.
        This cannot and will not rename a join action. "name" is ignored in
        the keywords.

        Args:
            guildname: Target guildname
            name: Target action to update
            [name], (optionals set by config)

        Keys: **See .create()

        Returns:
            {"status": true/false, "response": str}
        """

        logger.debug(f'update: {guildname} | {name} | {kwargs.items()}')
        results = self.read(guildname, name)
        if not(results["status"]):
            return {"status": False, "response": "Guild or Name not found"}
        config = results["response"]
        for key, value in kwargs.items():
            if (key in config) and (key != 'name'):
                config[key] = value

        for action in self.jaConfig[guildname]:
            if action["name"] == name:
                i = self.jaConfig[guildname].index(action)
                logger.info(f'Updating join action index: {i}')
                self.jaConfig[guildname][i] = config
                return {"status": True, "response": "Join action updated"}
        logger.warning(f'Something went wrong: name missing')
        return {"status": False, "response": "Something went wrong"}

    def delete(self, guildname: str, name: str) -> dict:
        """ Deletes a stored config for welcome messages

            Returns:
                {"status": true/false, "response": str}
        """
        logger.debug(f'deleteMessage: {guildname} | {name}')
        if not(guildname in self.jaConfig):
            logger.info('Guild not found')
            return {"status": False, "response": "Guild not found"}
        for n in self.jaConfig[guildname]:
            if n["name"] == name:
                logger.info(f'Deleting join action name: {name}')
                i = self.jaConfig[guildname].index(n)
                del self.jaConfig[guildname][i]
                return {"status": True, "response": "Join action deleted"}
        logger.info('Name not found')
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
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/joinActions.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            json_io.saveConfig(self.jaConfig, outFile)
        except json_io.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        return {"status": True, "response": "Config saved"}

    def getJoinMessage(self, guild: str, user: str) -> dict:
        """ Returns any join messages to send

        Args:
            guild: The guildname where the join even fired
            user: The discord.user.name of who joined (not nickname)

        Returns:
            {"status": True,
             "response":
                [{"message": "Message to send",
                 "channel": "ChannelName"},]
            }
            If status is fales, response contains reason why
            If channel is blank, the message is intended to be a DM

        Raises:
            None
        """

        joinMessages = []
        results = self.readAll(guild)
        if not(results["status"]):
            logger.info(f'Guild not configured: {guild}')
            return {"status": False, "response": "Guild not configured"}
        actions = results["response"]
        logger.debug(f'joinActions found: {actions}')

        for a in actions:
            if a["active"]:
                joinMessages.append({"message": a["message"],
                                     "channel": a["channel"]})
        if not(len(joinMessages)):
            return {"status": False, "response": "No join actions found"}
        return {"status": True, "response": joinMessages}

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
