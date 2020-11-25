""" Handle the consumption and processing of basic Channel commands

    Created by Preocts
        Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot

    A basic channel command is any command that has a static, or list fed,
    response and replies back into the chat where executed. Th
"""
import time
import json
import logging
import pathlib
from eggbot.utils import eggUtils

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return basicCommands()


class basicCommands:
    """ Defines the basicCommands class """
    name = 'basicCommands'
    allowReload = True
    instCount = 0

    # Default static defines
    COMMAND_KEYS = ('users', 'channels', 'roles', 'cooldown',
                    'lastran', 'text', 'help')
    COMMAND_DEFAULT = ([], [], [], 10, 0, '', '')
    COMMAND_DATATYPE = ('list', 'list', 'list',
                        'int', 'int', 'str', 'str')

    def __init__(self):
        """ Defines __init__ """
        logger.info('Initialize basicCommands')
        self.bcConfig = {}
        self.activeConfig = None
        self.loadConfig()
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
        self.saveConfig()
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
        """
        Scans a provided message for a command and return if found

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

        # While I'd like to assume my own configs are healthy and that nobody
        # would ever fuck with them... I'm not an ass and neither are you.
        self.checkGuild(guild)
        try:
            # Is this a command
            for t in self.bcConfig['guilds'][guild]['commands']:
                if message.lower().startswith(t, 0, len(t)):
                    cData = self.bcConfig['guilds'][guild]['commands'][t]
                    cName = t
                    break
            if cName is None:
                return {'status': False, 'response': 'No command found'}

            # Channel restrictions
            if len(cData['channels']) and not(channel in cData['channels']):
                return {'status': False, 'response': 'Channel restricted'}

            # User restrictions
            if len(cData['users']) and not(user in cData['users']):
                return {'status': False, 'response': 'User restricted'}

            # Role restrictions
            if len(cData['roles']):
                return {'status': False, 'response': 'Role restricted'}

            # Throttle restriction
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
        for key in basicCommands.COMMAND_KEYS:
            keyValue = basicCommands.COMMAND_DEFAULT[
                basicCommands.COMMAND_KEYS.index(key)]
            self.bcConfig['guilds'][guild]['commands'][cname][key] = keyValue

        # Set simple command
        logger.debug(f'Simple command: {cname} | {text}')
        self.bcConfig['guilds'][guild]['commands'][cname]['text'] = text

        return {
            'status': True,
            'response': f'"{cname}" is now set and ready to use.'}

    def modCommand(self, guild: str, msg: str) -> dict:
        """
        Modify a command that already exists

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
        if mod not in basicCommands.COMMAND_KEYS:
            return {
                'status': False,
                'response': f'Key "{mod}" is not a valid mod option.'}

        # Get the type for the targeted key
        tartype = basicCommands.COMMAND_DATATYPE[
            basicCommands.COMMAND_KEYS.index(mod)]

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
                self.bcConfig['guilds'][guild]['commands'][cname][mod] += int(text)  # noqa
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
                self.bcConfig['guilds'][guild]['commands'][cname][mod] = int(text)  # noqa
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
            if text not in self.bcConfig['guilds'][guild]['commands'][cname][mod]:  # noqa
                return {
                    'status': False,
                    'response': f'"{text}" was not found in "{mod}".'}
            ind = self.bcConfig['guilds'][guild]['commands'][cname][mod].index(text)  # noqa
            self.bcConfig['guilds'][guild]['commands'][cname][mod].pop(ind)

            return {
                'status': True,
                'response': f'"{mod}" Successfully modified.'}

    def delCommand(self, guild: str, msg: str) -> dict:
        """
        Delete a command

        Args:
            guild (str): The ID of the guild
            msg (str): The message content

        Returns:
            dict : {"status": bool, "response": str}

        Raises:
            None
        """
        logger.debug(f'delCommand: {guild} | {msg}')

        self.checkGuild(guild)

        # Command to delete
        command = msg.split(' ')[1].lower()

        if self.bcConfig['guilds'][guild]['commands'].get(command) is not None:
            del self.bcConfig['guilds'][guild]['commands'][command]
            return {'status': True, 'response': f'"{command}" deleted'}
        return {'status': False, 'response': f'"{command}" not found'}

    def commandList(self, guild: str, channel: str, roles: list,
                    user: str, message: str) -> dict:
        """
        Lists commands available to the requesting user

        Will not show commands that a user cannot access due to channel,
        role, or user exclusive mods. Outputs a command separated string
        nested in a code block. This system command has a self-defined one
        minute (60 seconds) timeout between uses on a channel level.

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
        logger.debug(f'commandList Start: {guild}, {channel}, {roles}, '
                     f'{user}, {message}')
        self.checkGuild(guild)

        # Check for listcontrol flag (do users need a role to run?)
        if self.bcConfig['guilds'][guild]['listcontrol']:
            allowedroles = self.bcConfig['guilds'][guild]['allowedroles']
            if allowedroles and not(any(role in allowedroles for role in roles)):  # noqa
                return {'status': False, 'response': 'Role restriction'}

        # Check for cooldown on list command
        cooldown = self.bcConfig['guilds'][guild]['listcooldown']
        lastran = self.bcConfig['guilds'][guild]['listlastran']
        if cooldown > 1 and (time.time() - lastran) < cooldown:
            return {'status': False, 'response': 'Cooldown active'}
        split_message = message.lower().split(' ')

        # Pull the second word, if provided, or assign None
        search_string = split_message[1] if len(split_message) > 1 else None
        guild_commands = self.bcConfig['guilds'][guild]['commands']
        command_list = []

        for command, values in guild_commands.items():
            # Channel restrictions?
            if values['channels'] and not(channel in values['channels']):
                continue
            # User restrictions?
            if values['users'] and not(user in values['users']):
                continue
            # Role restrictions?
            if values['roles']:
                if not(any(role in values['roles'] for role in roles)):
                    continue
            if search_string is not None:
                if not(command.startswith(search_string)):
                    continue
            command_list.append(command)
        if command_list:
            self.bcConfig['guilds'][guild]['listlastran'] = time.time()
        logger.debug('commandList Finish')
        return {'status': True, 'response': command_list}

    def commandHelp(self, guild: str, roles: list) -> dict:
        """
        Generates the help text for basicCommands

        Checks the same permissions that control settting/modding commands
        in the config (allowedroles). If the user does not hold the role
        the command will be skipped. If the allowedroles list is empty then
        anyone can run this command.

        Args:
            guild(str): The ID of the guild
            roles (List()): List of role IDs

        Returns:
            (dict) : {"status": True, "response": "command.content"}
        """
        logger.debug(f'commandHelp Start: {guild}, {roles}')
        self.checkGuild(guild)

        # Check for listcontrol flag (do users need a role to run?)
        if self.bcConfig['guilds'][guild]['listcontrol']:
            allowedroles = self.bcConfig['guilds'][guild]['allowedroles']
            if allowedroles and not(any(role in allowedroles for role in roles)):  # noqa
                return {'status': False, 'response': 'Role restriction'}

        response = "Basic Commands Module command list: ```" \
            "+ command!list (search)\n" \
            "\tList commands available in channel. Search is optional\n" \
            "+ command!add [command] [message]\n" \
            "\tCreates a command that will display defined message\n" \
            "+ command!del [command]\n" \
            "\tDeletes command (there is no undo)\n" \
            "+ command!mod [command] [-/+/-+] [flag] [value] \n" \
            "\tModify or replace flags of a command\n" \
            "\tValid flags are:\n" \
            "\t - users : Limit use of command to only these IDs\n" \
            "\t - channels: Limit use of command to only these channel IDs\n" \
            "\t - roles: Limit use of command to only these role IDs\n" \
            "\t - cooldown: How many seconds between each run of command\n" \
            "\t - text: Define what the command returns to chat\n" \
            "+ command!help\n" \
            "\tThis message```"
        return {'status': True, 'response': response}

    def loadConfig(self):
        """ Load a config into the class instance"""
        file_ = eggUtils.abs_path(__file__) + '/config/basicCommands.json'
        logger.debug(f'[START] loadConfig : {file_}')
        json_file = {}
        try:
            with open(file_, 'r') as load_file:
                json_file = json.load(load_file)
        except json.decoder.JSONDecodeError:
            logger.error('Config file empty or bad format. ', exc_info=True)
        except FileNotFoundError:
            logger.error(f'Config file not found: {file_}', exc_info=True)

        self.bcConfig = json_file
        self.activeConfig = file_
        logger.debug(f'[FINISH] loadConfig : {file_}')
        return

    def saveConfig(self) -> bool:
        """ Save a config into the class instance"""
        file_ = eggUtils.abs_path(__file__) + '/config/basicCommands.json'
        logger.debug(f'[START] saveConfig : {file_}')
        path = pathlib.Path('/'.join(file_.split('/')[:-1]))
        path.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_, 'w') as save_file:
                save_file.write(json.dumps(self.bcConfig, indent=4))
        except OSError:
            logger.error(f'File not be saved: {file_}', exc_info=True)
        logger.debug(f'[FINSIH] saveConfig : {file_}')
        return

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
        return clean_roles

    def guild_permissions(self, guild: str, user: str, channel: str) -> bool:
        """ Checks guild level permissions for command use """
        # Is this user prohibited
        if user in self.bcConfig['guilds'][guild]['restrictusers']:
            return {'status': False, 'response': 'User Prohibited'}
        # Is this channel prohibited
        if channel in self.bcConfig['guilds'][guild]['restrictchannels']:
            return {'status': False, 'response': 'Channel Prohibited'}
        return {'status': True, 'reponse': ''}

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
        # HOLD FOR RELEASE
        return

        chtype = kwargs.get('chtype')
        message = kwargs.get('message')
        message_slice = message.clean_content.split(' ')
        # This modules only deals with text channels
        if chtype != 'text':
            return
        guild = str(message.guild.id)
        user = str(message.author.id)
        channel = str(message.channel.id)
        roles = self.parseRoles(message.author.roles)
        msg = message.clean_content

        # Check against restrictchannels and restrictusers
        # Do not pass go, do not run commands, pay me 200 dollars V:
        if not(self.guild_permissions(guild, user, channel)['status']):
            return

        # Check for basicCommand control commands
        if "command!" in message_slice[0]:
            control = message_slice[0].replace('command!', '')
            results = None
            if control.lower() == 'add':
                results = self.addCommand(guild, msg)
            if control.lower() == 'mod':
                results = self.modCommand(guild, msg)
            if control.lower() == 'del':
                results = self.delCommand(guild, msg)
            if control.lower() == 'list':
                results = self.commandList(guild, channel, roles, user, msg)
                if results['status']:
                    outmessage = 'Available commands for: ' + \
                                 f'{message.author.display_name}'
                    outmessage += f'```{", ".join(results["response"])}```'
                    await message.channel.send(outmessage)
                    return
            if control.lower() == 'help':
                results = self.commandHelp(guild, roles)
            if results is not None:
                logger.debug(results)
                self.saveConfig()
                await message.channel.send(results['response'])
            return

        results = self.commandCheck(guild, channel, roles, user, msg)
        if results['status']:
            await message.channel.send(results['response'])
        else:
            logger.debug(f'commandCheck False: {results["response"]}')
        return

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
