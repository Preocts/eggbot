""" GuildConfig is a module for Egg_Bot to control guild level configuration

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord

    Refactor: 03/25/2020
"""
import logging
import json

logger = logging.getLogger(__name__)  # Create module level logger

# MODULE LEVEL STATICS FOR CONFIGUTATION
# Welcome Config keys:
VALID_KEYS_WELCOME = ('name', 'channel', 'roles', 'message')


class eggGuildConfig:
    """ Defines the eggGuildConfig class

        Config format:
        {
            "<GuildName>": {
                "welcomemessage": [ {
                    "content": "Message to display",
                    "toggle": true/false,
                    "target": "dm/channel",
                    "channel": "channelname",
                    "roles": "restrict to roles"
                }]
            }
        }
    """

    def __init__(self, inputFile="./config/guildConfig.json"):
        """ Define __init__ """
        self.guildConfig = {}
        self.activeConfig = ''
        self.loadConfig(inputFile)

    def __str__(self):
        return json.dumps(self.guildConfig, indent=4)

    def __bool__(self):
        if len(self.guildConfig):
            return True
        return False

    __nonzero__ = __bool__

    def addWelcomeConfig(self, guildname: str, **kwargs) -> dict:
        """ Adds a welcome message to the loaded config

        Sets the configuration of welcome messages. If keyword 'channel' is
        left blank then a direct message will be sent instead. A guild can
        have any number of welcome messages with unique names. Undefined
        args will be ignored

        Args:
            guildname: Target guildname
            [name], (optionals set by VALID_KEYS_WELCOME)

        Typical Usuage:
        DM Welcome:
            .addWelcomeConfig('GuildName', name='DMWelcome',
                              message='Welcome Message String here')
        Chat Welcome:
            .addWelcomeConfig('GuildName', name='Chat', channel='General',
                              message='Welcome Message String here')
        Custom Welcome:
            .addWelcomeConfig('GuildName', name='PatronChat',
                              channel='General', roles=['Patrons'],
                              message='Special Welcome for patreon roles')

        Returns:
            {"status": true/false, "response": str}
        """

        logger.debug(f'addWelcomeConfig: {guildname} | {kwargs.items()}')
        config = {}
        for key, value in kwargs.items():
            if key in VALID_KEYS_WELCOME:
                config[key] = value
        if not('name' in config):
            logger.error('"name" not provided for addWelcomeConfig')
            logger.debug(f'{guildname} | {kwargs.items()}')
            return {"status": False, "response": "Name not defined"}
        if not(guildname in self.guildConfig):
            self.guildConfig[guildname] = [config, ]
        else:
            for n in self.guildConfig[guildname]:
                if n["name"] == config["name"]:
                    logger.info(f'Name already exists: {config["name"]}')
                    return {"status": False, "response": "Name already exists"}
            self.guildConfig[guildname].append(config)
        logger.info(f'Guild Welcome added for {guildname}')
        logger.debug(f'{guildname} | {kwargs.items()}')
        return {"status": True, "response": "Welcome message created"}

    def deleteWelcomeConfig(self, guildname: str, name: str) -> dict:
        """ Deletes a stored config for welcome messages

            Returns:
                {"status": true/false, "response": str}
        """
        logger.debug(f'deleteWelcomeConfig: {guildname} | {name}')
        if not(guildname in self.guildConfig):
            return {"status": False, "response": "Guild not found"}
        for n in self.guildConfig[guildname]:
            if n["name"] == name:
                logger.info(f'Deleting welcome message name: {name}')
                i = self.guildConfig[guildname].index(n)
                del self.guildConfig[guildname][i]
                return {"status": True, "response": "Welcome message deleted"}
        return {"status": False, "response": "Welcome message name not found"}

    def loadConfig(self, inputFile: str) -> dict:
        """ Loads guildConfig configuration into memory"""

        try:
            with open(inputFile) as file:
                self.guildConfig = json.load(file)
        except json.decoder.JSONDecodeError:
            logger.error(f'guildConfig Config file empty ', exc_info=True)
        except FileNotFoundError:
            logger.error(f'guildConfig Config file not found '
                         '{inputFile}', exc_info=True)
            try:
                open(inputFile, 'w')
            except OSError:
                logger.critical('guildConfig failed to load. Closing. ',
                                exc_info=True)
                exit()
        self.activeConfig = inputFile
        return {"status": True, "response": "Config loaded"}

    def saveConfig(self, outputFile: str = None) -> dict:
        """ Writes guildConfig configuration to disk """

        if not(outputFile) and len(self.activeConfig) > 0:
            outputFile = self.activeConfig
        else:
            logger.warning(f'saveConfig: No file give: {outputFile}')
            return {"status": False, "response": "Missing filename"}
        try:
            with open(outputFile, 'w') as file:
                file.write(json.dumps(self.guildConfig, indent=4))
                logger.info(f'Success: guildConfig config '
                            'saved to {outputFile}')

        except OSError:
            logger.error(f'guildConfig Config file not saved to {outputFile}',
                         exc_info=True)
            return {"status": False, "response": "Error saving config"}
        return {"status": True, "response": "Config saved"}
