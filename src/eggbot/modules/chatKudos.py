""" Kudos system for Discord chat fun

    Created by Preocts
        Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot

    Grant points that have no more meaning than what you give them. Display
    leaderboard.

    Checklist:
    [x] Load config or create new
    [x] save config and create new file/path
    [x] Check for empty messages
    [x] Check for text channel messages only
    [x] Check if config has guild (build if needed)
    [x] Check if author.id is in config.guild.users
    [x] Check if author.roles is in config.guild.roles
    [x] Alternative "all in" allows all users to run kudos
    [x] Scan message for kudo! commands
        [x] kudo!help - display help
        [x] kudo!board (number) - show board, default 10 slots
        [x] kudo!set max [number] - set max +/- kudo amount
        [x] kudo!set user [@mention] - add/remove @user from control
        [x] kudo!set role [#role] - add/remove #role from control
        [x] kudo!set gain [message content] - set gain message
        [x] kudo!set loss [message content] - set loss message
        [x] kudo!set lock - toggle all users or limit users
    [x] Scan message for @mentions
    If found:
        [x] Return id, name, amount for each @mention in list
        [x] Apply points to config
        [x] Add max add/sub amount (Buzzkill)
        [x] Generate output
        [x] Info log line for later metrics [KUDO]
"""

import json
import logging
import pathlib
from eggbot.utils import eggUtils
from collections import namedtuple

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return chatKudos()


class chatKudos:
    """ Defines the chatKudos class """
    name = 'chatKudos'
    version = 'v1.0.0'
    allowReload = False
    instCount = 0
    kudos = namedtuple('kudos', ['id', 'name', 'amount'])

    def __init__(self):
        """ Defines __init__ """
        logger.info('Initialize chatKudos')
        self.ckConfig = {}
        self.activeConfig = None
        self.loadConfig()
        chatKudos.instCount += 1
        logger.info('chatKudos loaded.')
        return

    def __str__(self):
        return str(self.ckConfig)

    def __bool__(self):
        if len(self.ckConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        self.saveConfig()
        chatKudos.instCount -= 1
        return

    def loadConfig(self):
        """ Load a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/chatKudos.json'
        logger.debug(f'[START] loadConfig : {file_}')
        json_file = {}
        try:
            with open(file_, 'r') as load_file:
                json_file = json.load(load_file)
        except json.decoder.JSONDecodeError:
            logger.error('Config file empty or bad format. ', exc_info=True)
        except FileNotFoundError:
            logger.error(f'Config file not found: {file_}', exc_info=True)

        self.ckConfig = json_file
        self.activeConfig = file_
        logger.debug(f'[FINISH] loadConfig : {file_}')
        return

    def saveConfig(self) -> bool:
        """ Save a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/chatKudos.json'
        logger.debug(f'[START] saveConfig : {file_}')
        path = pathlib.Path('/'.join(file_.split('/')[:-1]))
        path.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_, 'w') as save_file:
                save_file.write(json.dumps(self.ckConfig, indent=4))
        except OSError:
            logger.error(f'File not be saved: {file_}', exc_info=True)
        logger.debug(f'[FINSIH] saveConfig : {file_}')
        return

    def checkConfig(self, guild):
        """
        Ensure the config is legit, add the guild if missing

        Args:
            [discord.guild] : Discord Guild class
        """
        guild_id = str(guild.id)
        owner_id = str(guild.owner_id)
        if not(isinstance(self.ckConfig, dict)):
            logger.warning('Config file was not a dict. Fixing')
            self.ckConfig = {}
            self.saveConfig()

        if self.ckConfig.get(guild_id) is None:
            logger.info(f'Adding guild to config: {guild_id}, {guild.name}')
            self.ckConfig[guild_id] = {
                'controls': {
                    'roles': [],
                    'users': [owner_id],
                    'lock': False,
                    'max': -1,
                    'gain-message': '{points} points to {name}!',
                    'loss-message': '{points} points from {name}!'
                },
                'scores': {}
            }
            self.saveConfig()

        if owner_id not in self.ckConfig[guild_id]['controls']['users']:
            self.ckConfig[guild_id]['controls']['users'].append(owner_id)
            self.saveConfig()

        return

    def generate_board(self, message: str) -> str:
        """
        Generates a list of top score holders

        Args:
            [str] : Discord clean message content that triggers this command

        Returns:
            [str] : Formatted response to send to channel
        """
        logger.debug(f'[START] generate_board : {message}')
        split = message.clean_content.split(' ')
        guild_id = str(message.guild.id)
        count = 10
        if len(split) > 1:
            try:
                count = int(split[1])
            except ValueError:
                pass
        # Get a list of keys to the dict sorting values lowest to highest
        sorted_keys = sorted(
            self.ckConfig[guild_id]['scores'],
            key=self.ckConfig[guild_id]['scores'].get
        )
        score_list = []
        name_list = []
        while count > 0 and sorted_keys:
            key = sorted_keys.pop(-1)
            display_name = "Not_Found"
            user = message.guild.get_member(int(key))
            if user is not None:
                display_name = user.display_name
            score_list.append(self.ckConfig[guild_id]['scores'][key])
            name_list.append(display_name)
            count -= 1
        leader_board = [f'Top {len(name_list)} kudo holders:```']
        for name, score in zip(name_list, score_list):
            basestr = '{:>5} | {:<38}\n'
            leader_board.append(basestr.format(score, name[:38]))
        leader_board.append('```')
        return ''.join(leader_board)

    def find_kudos(self, message) -> tuple:
        """
        Scans the message for mentions and looks for kudos

        Args:
            message [discord.message] : Discord message class

        Returns:
            [namedtuple] : (chatKudos.kudos)
        """
        logger.debug(f'[START] find_kudos : {message}')
        max_ = self.ckConfig[str(message.guild.id)]['controls']['max']
        results = []
        for mention in message.mentions:
            logger.debug(f'Found mention: {mention}')
            target = str(mention.id)
            for idx, word in enumerate(message.content.split()):
                if target in word.strip('<').strip('>').strip('#').strip('!'):
                    try:
                        next_word = message.content.split()[idx + 1]
                    except IndexError:
                        continue
                    if '+' not in next_word and '-' not in next_word:
                        continue

                    point_change = next_word.count('+') - next_word.count('-')
                    if max_ > 0 < point_change > max_:
                        point_change = max_
                    elif max_ > 0 > point_change < (max_ * -1):
                        point_change = max_ * -1

                    results.append(chatKudos.kudos(
                        target, mention.display_name, point_change))
        return tuple(results)

    def apply_kudos(self, guild: str, target: str, amount: int) -> int:
        """
        Handles granting, removing points to users.

        Checks config [guild][controls][max] for maximum change amount and
        will limit the change to that amount if set greater than 0.

        Args:
            [str] : Discord guild ID
            [str] : Discord user ID of target for action
            [int] : Value of points being applied (can be negative)

        Returns:
            [int] : Actual points applied after max adjustment
        """
        logger.debug(f'[START] kudoMath : {guild}, {target}, {amount}')
        currentpoints = self.ckConfig[guild]['scores'].get(target, 0)
        self.ckConfig[guild]['scores'][target] = currentpoints + amount
        self.saveConfig()
        logger.debug(f'[FINISH] kudoMath : {amount}')
        return amount

    def parse_command(self, message) -> str:
        """ Parses a kudo!set request, directs flow to correct CLI handler """
        logger.debug(f'[START] parse_command : {message}')
        guild_id = str(message.guild.id)
        message_pieces = message.clean_content.split()
        response = ''

        if len(message_pieces) == 1:
            logger.debug('[FINISH] parse_command : missing required options')
            return response
        command = message_pieces[1].lower()
        try:
            options = message_pieces[2:]
        except IndexError:
            options = []

        if command == 'max' and options:
            response = self.set_max(guild_id, options[0])
        if command == 'user':
            response = self.set_lists(guild_id, message)
        if command == 'role':
            response = self.set_lists(guild_id, message)
        if command == 'gain':
            response = self.set_message(guild_id, options, 'gain')
        if command == 'loss':
            response = self.set_message(guild_id, options, 'loss')
        if command == 'lock':
            response = self.set_lock(guild_id)
        return response

    def set_lock(self, guild_id: str) -> str:
        """ CLI : Toggles the lock flag in config """
        flag = not(self.ckConfig[guild_id]['controls']['lock'])
        self.ckConfig[guild_id]['controls']['lock'] = flag
        if flag:
            return 'Lock is engaged. Only allowed users/roles can Kudos.'
        return 'Lock is disengaged. Everyone can Kudos!'

    def set_max(self, guild_id: str, value: str) -> str:
        """ CLI : Sets the max point adjustment for Kudos """
        logger.debug(f'[START] set_max : {guild_id}, {value}')
        try:
            self.ckConfig[guild_id]['controls']['max'] = int(value)
        except ValueError:
            logger.debug(f'[FINISH] set_max : not int, {value}')
            response = f'Error: {value} is not a number.'
            return response
        response = f'Max point adjustment now set to **{value}**'
        logger.debug('[FINSIH] set_max :')
        return response

    def set_lists(self, guild_id: str, message) -> str:
        """ CLI : Add/Remove user/role ID from allow lists """
        logger.debug(f'[START] set_lists : {guild_id}, {message}')
        results = []
        response = ''
        # Search for user mentions
        for mention in message.mentions:
            if str(mention.id) in self.ckConfig[guild_id]['controls']['users']:
                idx = self.ckConfig[guild_id]['controls']['users'].index(
                    str(mention.id))
                self.ckConfig[guild_id]['controls']['users'].pop(idx)
                results.append('**-**' + mention.display_name)
                continue
            self.ckConfig[guild_id]['controls']['users'].append(
                str(mention.id))
            results.append('**+**' + mention.display_name)

        # Search for role mentions
        for mention in message.role_mentions:
            if str(mention.id) in self.ckConfig[guild_id]['controls']['roles']:
                idx = self.ckConfig[guild_id]['controls']['roles'].index(
                    str(mention.id))
                self.ckConfig[guild_id]['controls']['roles'].pop(idx)
                results.append('**-**' + mention.name)
                continue
            self.ckConfig[guild_id]['controls']['roles'].append(
                str(mention.id))
            results.append('**+**' + mention.name)

        if results:
            response = 'Allow list changes: ' + ', '.join(results)
        logger.debug(f'[FINISH] set_lists : {response}')
        return response

    def set_message(self, guild_id: str, values: str, msg_type: str) -> str:
        """ CLI : Update reply messages for kudo gain/loss """
        logger.debug(f'[START] set_message : {guild_id}, {values}, {msg_type}')
        response = ''
        new_message = ' '.join(values)
        if msg_type == 'gain':
            self.ckConfig[guild_id]['controls']['gain-message'] = new_message
            response = f'New gain message set: "{new_message}"'
        if msg_type == 'loss':
            self.ckConfig[guild_id]['controls']['loss-message'] = new_message
            response = f'New loss message set: "{new_message}"'
        logger.debug(f'[FINISH] set_message : {response}')
        return response

    def format_help(self) -> str:
        """ CLI : Returns pretty format of help """
        help_lines = [
            f'Chat Kudos {chatKudos.version} help: Basics',

            '```@mention +++ @mention ---',
            '\tGrants or removes kudos from mentioned user',
            '\nkudo!board (# of results)',
            '\tShow Top Scores board, defaults to 10 results',
            '\nkudo!help',
            '\tDisplay this help```',
            'Chat Kudos help: Config Options',

            '```Only allowed users can access config options.',
            'Server owner is always allowed.',

            '\nkudo!set max [#]',
            '\tSets maximum +/- kudo amount per request (BuzzKill mode)',
            '\tSet this to 0 or -1 to remove restriction',

            '\nkudo!set gain [message to display on gain]',
            'kudo!set loss [message to display on loss]',
            '\tSet gain or loss message that is displayed',
            '\t"{points}" will be replaced with # of points',
            '\t"{name}" will be replaced with user\'s display name',

            '\nkudo!set user [@mention] (@mention)...',
            'kudo!set role [@role_name] (@role_name)...',
            '\tAdd/remove @user(s)/@roles to the allow lists',
            '\tAdds if not on the list, removes if already on list',

            '\nkudo!set lock',
            '\tTurns lock on or off. When locked only allowed users/roles '
            'can use Kudos. Server owner always has access.```'
        ]
        return '\n'.join(help_lines)

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
        Supported_Channels = ("<class 'discord.channel.TextChannel'>")
        message = kwargs.get('message')
        if message is None:
            logger.debug('[FINISH] onMessage : incoming message empty')
            return

        if str(type(message.channel)) not in Supported_Channels:
            logger.debug('[FINISH] onMessage : Channel type not supported')
            return

        self.checkConfig(message.guild)
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        user_roles = set([role.id for role in message.author.roles])
        config_roles = set(self.ckConfig[guild_id]['controls']['roles'])
        loss_response = self.ckConfig[guild_id]['controls']['loss-message']
        gain_response = self.ckConfig[guild_id]['controls']['gain-message']
        allowed_user = False
        allowed_role = False

        if user_roles.intersection(config_roles):
            allowed_role = True

        if user_id in self.ckConfig[guild_id]['controls']['users']:
            allowed_user = True

        if self.ckConfig[guild_id]['controls']['lock'] and not(
                any([allowed_role, allowed_user])):
            logger.debug('[FINISH] onMessage : User/Role not in allowed list')
            return

        ##########################
        # Module Command Catches #
        ##########################
        response = ""
        first_word = message.clean_content.split()[0].lower()
        if first_word == 'kudo!help':
            response = self.format_help()
            # This has a unique hanndler as we want to send this to DM
            await message.author.create_dm()
            await message.author.dm_channel.send(response)
            response = ""
        if first_word == 'kudo!board':
            response = self.generate_board(message)
        if first_word == 'kudo!set' and allowed_user:
            response = self.parse_command(message)
        if response:
            await message.channel.send(response)
            self.saveConfig()

        ########################
        # Scan and apply Kudos #
        ########################
        if message.mentions:
            kudo_list = self.find_kudos(message)
            for values in kudo_list:
                points = self.apply_kudos(guild_id, values.id, values.amount)
                logger.info(f'[KUDO] {guild_id}, {user_id}, '
                            f'{values.id}, {values.amount}')
                out_message = gain_response
                if values.amount <= 0:
                    out_message = loss_response
                if not(out_message):
                    continue
                await message.channel.send(out_message.format(
                    points=str(points), name=values.name))

            logger.debug(f'[FINISH] onMessage : Processed {len(kudo_list)} kudos')  # noqa
            return

        logger.debug('[FINISH] onMessage : No actions')
        return

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
