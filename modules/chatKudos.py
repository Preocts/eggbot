""" Point system for in-chat acknowledgements

    Created by Preocts
        Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot

    Grant points that have no more meaning than what you give them. Display
    leaderboard. More to come.

    Checklist:
    [x] Check for empty messages
    [x] Check for text channel messages only
    [x] Check if config has guild (build if needed)
    [x] Check if author.id is in config.guild.users
    [] Alternative "all in" allows all users to run kudos
    [] Scan message for kudo! commands
        [x] kudo!board (number) - show board, default 10 slots
        [x] kudo!set max [number] - set max +/- kudo amount
        [x] kudo!set user (+/-) [@mention] - add/remove @user from control
        [x] kudo!set message (+/-) [message content] - set gain/loss messages
        [x] kudo!help - display help
        [] kudo!set ?????? - toggle all users or limit users
    [x] Scan message for @mentions
    If found:
        [x] Return id, name, amount for each @mention in list
        [x] Apply points to config
        [x] Add max add/sub amount (Buzzkill)
        [x] Generate output
        [x] Info log line for later metrics [KUDO]
"""

import logging
from utils import jsonIO
from collections import namedtuple

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return chatKudos()


class chatKudos:
    """ Defines the chatKudos class """
    name = 'chatKudos'
    allowReload = False
    instCount = 0
    kudos = namedtuple('kudos', ['id', 'name', 'amount'])

    def __init__(self, inFile: str = './config/chatKudos.json'):
        """ Defines __init__ """
        logger.info(f'Initialize chatKudos: {inFile}')
        self.ckConfig = {}
        self.activeConfig = None
        self.loadConfig(inFile)
        chatKudos.instCount += 1
        logger.info(f'Config loaded with {len(self.ckConfig)}')
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
        if self.activeConfig is None:
            logger.warn('Lost activeConfig name while closing, not good.')
            logger.info('Dump file attempt: ./config/chatKudos_DUMP.json')
            self.activeConfig = "./config/chatKudos_DUMP.json"
        self.saveConfig(self.activeConfig)
        chatKudos.instCount -= 1
        return

    def loadConfig(self, inFile: str = "./config/chatKudos.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.ckConfig = jsonIO.loadConfig(inFile)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {'status': False, 'response': 'Error loading config'}
        self.activeConfig = inFile
        logger.debug(f'loadConfig success: {inFile}')
        return {'status': True, 'response': 'Config Loaded'}

    def saveConfig(self, file: str = "./config/chatKudos.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {file}')
        try:
            jsonIO.saveConfig(self.ckConfig, file)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'saveConfig success: {file}')
        return {'status': True, 'response': 'Config saved'}

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
            self.saveConfig(self.activeConfig)

        if self.ckConfig.get(guild_id) is None:
            logger.info(f'Adding guild to config: {guild_id}, {guild.name}')
            self.ckConfig[guild_id] = {
                'controls': {
                    'roles': [],
                    'users': [owner_id],
                    'mysteryflag': False,
                    'max': -1,
                    'gain-message': '{points} points to {name}!',
                    'loss-message': '{points} points from {name}!'
                }
            }
            self.saveConfig(self.activeConfig)

        if owner_id not in self.ckConfig[guild_id]['controls']['users']:
            self.ckConfig[guild_id]['controls']['users'].append(owner_id)
            self.saveConfig(self.activeConfig)

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
        self.saveConfig(self.activeConfig)
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
        command = message_pieces[1]
        try:
            options = message_pieces[2:]
        except IndexError:
            options = []

        if command == 'max' and options:
            response = self.set_max(guild_id, options[0])
        if command == 'user' and message.mentions:
            response = self.set_user(guild_id, message.mentions, options[0])
        if command == 'message' and options:
            response = self.set_message(guild_id, options)

        return response

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

    def set_user(self, guild_id: str, mentions, action: str) -> str:
        """ CLI : Add/Remove user ID from config users list """
        logger.debug(f'[START] set_user : {guild_id}, {mentions}, {action}')
        results = []
        response = ''
        for mention in mentions:
            if action == '+':
                if str(mention.id) not in self.ckConfig[guild_id]['controls']['users']:  # noqa
                    self.ckConfig[guild_id]['controls']['users'].append(
                        str(mention.id))
            elif action == '-':
                try:
                    idx = self.ckConfig[guild_id]['controls']['users'].index(
                        str(mention.id))
                except ValueError:
                    pass
                self.ckConfig[guild_id]['controls']['users'].pop(idx)
            else:
                continue
            results.append(mention.display_name)
        if results:
            if action == '+':
                response = 'Added: ' + ', '.join(results)
            else:
                response = 'Removed: ' + ', '.join(results)
        logger.debug(f'[FINISH] set_user : {response}')
        return response

    def set_message(self, guild_id: str, values: str) -> str:
        """ CLI : Update reply messages for kudo gain/loss """
        logger.debug(f'[START] set_message : {guild_id}, {values}')
        response = ''
        new_message = ' '.join(values[1:])
        if values[0] == '+':
            self.ckConfig[guild_id]['controls']['gain-message'] = new_message
            response = f'New gain message set: "{new_message}"'
        elif values[0] == '-':
            self.ckConfig[guild_id]['controls']['loss-message'] = new_message
            response = f'New loss message set: "{new_message}"'
        logger.debug(f'[FINISH] set_message : {response}')
        return response

    def format_help(self) -> str:
        """ CLI : Returns pretty format of help """
        help_lines = [
            'kudo!help',
            '\tDisplay this help',
            'kudo!board (# of results)',
            '\tShow Top Scores board, defaults to 10 results',
            'kudo!set ??????',
            '\t*Toggle* : Allow all users access or restrict to user list',
            'kudo!set max [#]',
            '\tSets maximum +/- kudo amount per request (BuzzKill mode)',
            '\tSet this to 0 or -1 to remove restriction',
            'kudo!set user [+/-] [@mention]',
            '\tAdd (+) or Remove (-) @user from allowed users',
            'kudo!set message [+/-] [message content]',
            '\tSet gain/loss message when kudos are given or taken',
            '\tSetting this to be empty will silence in-chat responses'
        ]
        return 'Chat Kudos help:\n```' + '\n'.join(help_lines) + '```'

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

        loss_response = self.ckConfig[guild_id]['controls']['loss-message']
        gain_response = self.ckConfig[guild_id]['controls']['gain-message']

        if user_id not in self.ckConfig[guild_id]['controls']['users']:
            logger.debug('[FINISH] onMessage : User not in allowed list')
            return

        ##########################
        # Module Command Catches #
        ##########################
        response = ""
        if message.clean_content.split()[0] == 'kudo!set':
            response = self.parse_command(message)
        if message.clean_content.split()[0] == 'kudo!help':
            response = self.format_help()
        if message.clean_content.split()[0] == 'kudo!board':
            response = self.generate_board(message)
        if response:
            await message.channel.send(response)
            self.saveConfig(self.activeConfig)

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
