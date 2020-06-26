""" Point system for in-chat acknowledgements

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    Grant points that have no more meaning than what you give them. Display
    leaderboard. More to come.

    Checklist
    [x] capture ++++ after @
    [] command options
       - kudo!board (number)  * show board, default 5 slots, max 20
"""

import logging
from utils import jsonIO

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return chatKudos()


class chatKudos:
    """ Defines the chatKudos class """
    name = 'chatKudos'
    allowReload = False
    instCount = 0

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

    def checkConfig(self, guild: str):
        """ Ensure the config is legit, add the guild if missing """
        if not(isinstance(self.ckConfig, dict)):
            logger.warning('Config file was not a dict. Fixing')
            self.ckConfig = {}
            self.saveConfig(self.activeConfig)

        if self.ckConfig.get('controls') is None:
            self.ckConfig = {
                'controls': {
                    'users': [],
                    'gain-message': "{} points to {}!",
                    'loss-message': "{} points from {}!"
                }
            }
            self.saveConfig(self.activeConfig)
        if self.ckConfig.get(guild) is None:
            logger.info(f'Adding guild to config: {guild}')
            self.ckConfig[guild] = {}
            self.saveConfig(self.activeConfig)
        return

    def kudoMath(self, guild: str, user: str, target: str, amount: int):
        """
        Handles granting, removing points to users.

        Args:
            [str] : Discord guild ID
            [str] : Discord user ID of user
            [str] : Discord user ID of target for action
            [int] : Value of points being applied (can be negative)

        Returns:
            None
        """
        logger.debug(f'[START] kudoMath: {guild}, {user}, {target}')
        currentpoints = self.ckConfig[guild].get(target, 0)
        self.ckConfig[guild][target] = currentpoints + amount
        logger.info(f'[KUDO] {guild}, {user}, {target}')
        logger.debug('[FINISH] kudoMath')
        return

    def generate_board(self, guild: str, message: str, client) -> str:
        """
        Generates a list of top score holders

        Args:
            [str] : Discord guild ID
            [str] : Discord clean message content that triggers this command
            [obj] : Connected Discord client for name lookup

        Returns:
            [str] : Formatted response to send to channel
        """
        logger.debug(f'[START] generate_board: {guild}, {message}')
        split = message.split(' ')
        count = 10
        if len(split) > 1:
            try:
                count = int(split[1])
            except ValueError:
                pass
        # Get a list of keys to the dict sorting values lowest to highest
        sorted_keys = sorted(
            self.ckConfig[guild], key=self.ckConfig[guild].get)
        score_list = []
        name_list = []
        while count > 0 and sorted_keys:
            key = sorted_keys.pop(-1)
            display_name = "Not_Found"
            user = client.get_user(int(key))
            if user is not None:
                display_name = user.display_name
            score_list.append(self.ckConfig[guild][key])
            name_list.append(display_name)
            count -= 1
        leader_board = [f'Top {len(name_list)} kudo holders:```']
        for name, score in zip(name_list, score_list):
            basestr = '{:>10} | {:<30}\n'
            leader_board.append(basestr.format(score, name[:30]))
        leader_board.append('```')
        return ''.join(leader_board)

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
        # Only Guild Chat (text) support
        logger.debug('[START] onMessage')
        if not(kwargs.get('chtype') == 'text'):
            logger.debug('[FINISH] onMessage - not chat channel')
            return

        message = kwargs.get('message')
        if message is None:
            logger.debug('[FINISH] onMessage - no message')
            return
        client = kwargs.get('client')
        guild = str(message.guild.id)
        user = str(message.author.id)
        self.checkConfig(guild)
        loss_response = self.ckConfig['controls']['loss-message']
        gain_response = self.ckConfig['controls']['gain-message']
        if user not in self.ckConfig['controls']['users']:
            logger.debug('[FINISH] onMessage - user not allowed')
            return
        for mention in message.mentions:
            logger.debug(f'Found mention: {mention.id}')
            target = str(mention.id)
            for idx, word in enumerate(message.content.split(' ')):
                if target in word.strip('<').strip('>').strip('#').strip('!'):
                    try:
                        next_word = message.content.split(' ')[idx + 1]
                    except IndexError:
                        continue
                    if '+' not in next_word and '-' not in next_word:
                        continue
                    display_name = "Not_Found"
                    user = client.get_user(int(target))
                    if user is not None:
                        display_name = user.display_name
                    start_total = self.ckConfig[guild].get(target, 0)
                    self.kudoMath(
                        guild, user, target, next_word.count("+")
                    )
                    self.kudoMath(
                        guild, user, target, -(next_word.count("-"))
                    )
                    final_total = self.ckConfig[guild].get(target, 0)
                    diff_total = final_total - start_total
                    self.saveConfig(self.activeConfig)
                    if diff_total <= 0:
                        # Sad message here
                        await message.channel.send(loss_response.format(
                            str(diff_total), display_name))
                        return
                    await message.channel.send(gain_response.format(
                        str(diff_total), display_name))

        if message.clean_content.split()[0] == 'kudo!board':
            response = self.generate_board(
                guild, message.clean_content, client)
            if response:
                await message.channel.send(response)
        return

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
