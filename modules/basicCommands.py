""" Handle the consumption and processing of basic Channel commands

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    A basic channel command is any command that has a static, or list fed,
    response and replies back into the chat where executed. Th
"""
import time
import logging
from . import jsonIO
from utils import eggUtils

logger = logging.getLogger('default')  # Create module level logger

GUILD_TEMPLATE = {'restrictchannels': [],
                  'restrictusers': [],
                  'commands': {}}
COMMAND_KEYS = ['users', 'channels', 'roles', 'cooldown',
                'lastran', 'text', 'help']
COMMAND_DEFAULT = [[], [], [], 10, 0, '', '']
COMMAND_DATATYPE = ['list', 'list', 'list',
                    'int', 'int', 'str', 'str']


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return basicCommands()


class basicCommands:
    """ Defines the basicCommands class """
    name = 'basicCommands'
    allowReload = True
    instCount = 0

    def __init__(self, inFile: str = './config/basicCommands.json'):
        """ Defines __init__ """
        logger.info(f'Initialize basicCommands: {inFile}')
        self.bcConfig = {}
        self.activeConfig = None
        self.loadConfig(inFile)
        basicCommands.instCount += 1
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
        basicCommands.instCount -= 1
        return

    def checkConfig(self):
        """ Ensures config state is correctly formated """
        if 'restrictguilds' not in self.bcConfig.keys():
            logger.warning('checkConfig: Missing "restrictguilds" key')
            self.bcConfig['restrictguilds'] = []
        if 'guilds' not in self.bcConfig.keys():
            logger.warning('checkConfig: Missing "guilds" key')
            self.bcConfig['guilds'] = {}
        return

    def checkGuild(self, guildID: str):
        """ Creates a guild if it does not exist in the config

        Args:
            guildID(str): Numerical ID of the guild

        Returns:
            None

        Raises:
            None
        """
        # Ensure top-level exists
        self.checkConfig()
        if guildID not in self.bcConfig['guilds'].keys():
            guildSchema = {
                'prohibitedchannels': [],
                'prohibitedusers': [],
                'guildCommands': {}
            }
            self.bcConfig['guilds'][guildID] = guildSchema
        return

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
                  - If defined, is this from an allowed ["user"]
                  - If defined, is this from an allowed ["role"]
                  - If defined, is the command throttled
            If all of these pass you get Returns.

            Args:
                guildID (str): The ID of the guild
                channelID (str): The ID of the channel
                roleIDs (List(str)): List of role IDs
                userID (str): The ID of the user
                message (str): The message to scan for a command.

            Returns:
                (dict) : Two results based on pass/fail
                    {"status": True, "response": "command.content"}
                    {"status": False, "response": "[reason]"}

            Raises:
                None
        """
        logger.debug(f'{guild} | {channel} | {roles} | {user} | {message}')
        cData = None
        cName = None
        clean_roles = self.parseRoles(roles)
        self.checkGuild(guild)

        # While I'd like to assume my own configs are healthy and that nobody
        # would ever fuck with them... I'm not an ass and neither are you.
        try:
            # Is this user prohibited?
            if user in self.bcConfig['guilds'][guild]['restrictusers']:
                return {'status': False, 'response': 'User Prohibited'}
            # Is this channel prohibited?
            if channel in self.bcConfig['guilds'][guild]['restrictchannels']:
                return {'status': False, 'response': 'Channel Prohibited'}
            # Is this a command?
            for t in self.bcConfig['guilds'][guild]['commands']:
                if message.lower().startswith(t, 0, len(t)):
                    cData = self.bcConfig['guilds'][guild]['commands'][t]
                    cName = t
                    break
            if cName is None:
                return {'status': False, 'response': 'No command found'}

            # Channel restrictions?
            if len(cData['channels']) and not(channel in cData['channels']):
                return {'status': False, 'response': 'Channel restricted'}

            # User restrictions?
            if len(cData['users']) and not(user in cData['users']):
                return {'status': False, 'response': 'User restricted'}

            # Role restrictions?
            if len(cData['roles']) and not(clean_roles in cData['roles']):
                return {'status': False, 'response': 'Role restricted'}

            # Throttle restriction?
            if (time.time() - cData['lastran']) < cData['cooldown']:
                return {'status': False, 'response': 'Cooldown active'}
        except KeyError as msg:
            logger.error(f'Key error in conifg: {msg}')
            return {'status': False, 'response': 'Bad Config file, fix it!'}

        self.bcConfig['guilds'][guild]['commands'][cName]['lastran'] = time.time()  # noqa: E501
        logger.debug(f'Command returned: {cData["text"]}')
        return {'status': True, 'response': cData['text']}

    def addCommand(self, guild: str, msg: str) -> dict:
        """ Add a command to the config unless it already exists

        Args:
            guild (str): The ID of the guild
            msg (str): The message content

        Expected msg format:
            [!trigger] [commandName] [text command will display]

        Returns:
            dict : {"status": bool, "response": str}

        Raises:
            None
        """
        logger.debug(f'addCommand: {guild} | {msg}')
        if len(msg.split(' ')) < 3:
            return {
                'status': False,
                'response': 'Not enough input to create a command'}

        self.checkGuild(guild)

        # New command name
        cname = msg.split(' ')[1].lower()
        # Command text
        text = ' '.join(msg.split(' ')[2:])

        if cname in self.bcConfig['guilds'][guild]['commands'].keys():
            return {
                'status': False,
                'response': f'Command "{cname}" already exists.'}

        self.bcConfig['guilds'][guild]['commands'][cname] = {}
        for key in COMMAND_KEYS:
            keyValue = COMMAND_DEFAULT[COMMAND_KEYS.index(key)]
            self.bcConfig['guilds'][guild]['commands'][cname][key] = keyValue

        # Set simple command
        logger.debug(f'Simple command: {cname} | {text}')
        self.bcConfig['guilds'][guild]['commands'][cname]['text'] = text

        return {
            'status': True,
            'reponse': f'"{cname}" is now set and ready to use.'}

    def modCommand(self, guild: str, msg: str) -> dict:
        """ Modify a command that already exists

        Args:
            guild (str): The ID of the guild
            msg (str): The message content

        Expected msg format:
            [!trigger] [commandName] [(-, +, -+)key] [input]

        Returns:
            dict : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'modCommand: {guild} | {msg}')

        if len(msg.split(' ')) < 4:
            return {
                'status': False,
                'response': 'Not enough input to modify a command.'}

        self.checkGuild(guild)

        # New command name
        cname = msg.split(' ')[1].lower()
        # mod type requested
        mod = msg.split(' ')[2].lower()
        # Command text
        text = ' '.join(msg.split(' ')[3:])

        if cname not in self.bcConfig['guilds'][guild]['commands'].keys():
            return {
                'status': False,
                'response': f'Command "{cname}" does not exist.'}

        # Collect the type of modification:
        modtype = None
        if mod.startswith('-+'):
            mod = mod.lstrip('-+')
            modtype = 'replace'
        if modtype is None and mod.startswith('-'):
            mod = mod.lstrip('-')
            modtype = 'remove'  # Onle works for lists
        if modtype is None:
            mod = mod.lstrip('+')
            modtype = 'append'  # Adds to list, concats str, calc ints

        # Ensure we are modding a key that is valid
        if mod not in COMMAND_KEYS:
            return {
                'status': False,
                'response': f'Key "{mod}" is not a valid mod option.'}

        # Get the type for the targeted key
        tartype = COMMAND_DATATYPE[COMMAND_KEYS.index(mod)]

        if modtype == "append":
            if tartype == 'list':
                # Split the input into a list, strip spaces
                li = [w.strip() for w in text.split(',')]
                # Append assign
                self.bcConfig['guilds'][guild]['commands'][cname][mod] += li
            if tartype == 'int':
                if not(eggUtils.isInt(text)):
                    return {
                        'status': False,
                        'response': f'Value "{text}" is not a number.'}
                self.bcConfig['guilds'][guild]['commands'][cname][mod] += int(text)
            if tartype == 'str':
                # This can be done in one line, but a long line
                pt = self.bcConfig['guilds'][guild]['commands'][cname][mod]
                nt = ' '.join([pt, text.strip()])
                self.bcConfig['guilds'][guild]['commands'][cname][mod] = nt
            return {
                'status': True,
                'response': f'"{mod}" Successfully appended.'}

        if modtype == "replace":
            if tartype == 'list':
                # Split the input into a list, strip spaces
                li = [w.strip() for w in text.split(',')]
                # Direct assign
                self.bcConfig['guilds'][guild]['commands'][cname][mod] = li
            if tartype == 'int':
                if not(eggUtils.isInt(text)):
                    return {
                        'status': False,
                        'response': f'Value "{text}" is not a number.'}
                self.bcConfig['guilds'][guild]['commands'][cname][mod] = int(text)
            if tartype == 'str':
                self.bcConfig['guilds'][guild]['commands'][cname][mod] = text
            return {
                'status': True,
                'response': f'"{mod}" Successfully replaced.'}

        if modtype == 'remove':
            if not(tartype == 'list'):
                return {
                    'status': False,
                    'response': f'"-" flag cannot be used for {mod} key.'}
            if text not in self.bcConfig['guilds'][guild]['commands'][cname][mod]:
                return {
                    'status': False,
                    'response': f'"{text}" was not found in "{mod}".'}
            ind = self.bcConfig['guilds'][guild]['commands'][cname][mod].index(text)
            self.bcConfig['guilds'][guild]['commands'][cname][mod].pop(ind)

            return {
                'status': True,
                'response': f'"{mod}" Successfully modified.'}

    def loadConfig(self, inFile: str = "./config/basicCommands.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.bcConfig = jsonIO.loadConfig(inFile)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {'status': False, 'response': 'Error loading config'}
        self.activeConfig = inFile
        logger.debug(f'loadConfig success: {inFile}')
        return {'status': True, 'response': 'Config Loaded'}

    def saveConfig(self, file: str = "./config/basicCommands.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {file}')
        try:
            jsonIO.saveConfig(self.bcConfig, file)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'saveConfig success: {file}')
        return {'status': True, 'response': 'Config saved'}

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
        if len(discord_roles):
            for r in discord_roles:
                clean_roles.append(str(r.id))
        # logging.debug(f'parseRoles: {clean_roles}')
        return clean_roles

    async def onMessage(self, **kwargs) -> bool:
        """
        Hook method to be called from core script on Message event

        Keyword Args:
            chtype (str) : Either "text" or "dm" or "group"
            message (discord.message) : a discord.message class

        Returns:
            (boolean)

        Raises:
            None
        """
        chtype = kwargs.get('chtype')
        message = kwargs.get('message')
        # This modules only deals with text channels
        if chtype != 'text':
            return

        results = self.commandCheck(str(message.guild.id),
                                    str(message.channel.id),
                                    message.author.roles,
                                    str(message.author.id),
                                    message.clean_content)
        if results['status']:
            await message.channel.send(results['response'])
        else:
            logger.debug(f'commandCheck False: {results["response"]}')
        return


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
