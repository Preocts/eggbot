""" Fun things that happen when everyone gets involved

    Created by Preocts
        Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot

    #BlameNay
"""
import json
import time
import logging
import pathlib
from eggbot.utils import eggUtils

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return typingReact()


class typingReact:
    """ Defines the typingReact class """

    name = "typingReact"
    allowReload = True
    instCount = 0

    def __init__(self):
        logger.info('Initialize typingReact')
        self.trConfig = {}
        self.activeConfig = None
        self.tracktyping = []
        self.loadConfig()
        self.lastin = 0
        typingReact.instCount += 1
        logger.info('Config loaded.')
        return

    def __str__(self):
        return str(self.trConfig)

    def __bool__(self):
        if len(self.trConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        self.saveConfig()
        typingReact.instCount -= 1
        return

    def checkSys(self) -> bool:
        """ Creates a system record if it does not exist in the config """
        if "SYS-Rec" in self.trConfig.keys():
            return True
        sysSchema = {
            "SYS-Rec": {
                'optoutGuilds': [],
            }
        }
        self.trConfig = sysSchema
        return True

    def checkGuild(self, guildID: str) -> bool:
        """ Creates a guild if it does not exist in the config """
        self.checkSys()
        if guildID in self.trConfig.keys():
            return True
        self.trConfig[guildID] = {
            "cooldown": 86400,
            "piles": [
                {
                    "peak": 5,
                    "msg": "**SEVERAL PEOPLE ARE TYPING** :eyes:",
                    "lastran": 0
                },
                {
                    "peak": 10,
                    "msg": "*begins to sweat, inches toward the door*",
                    "lastran": 0
                },
                {
                    "peak": 15,
                    "msg": ":crystal_ball: Will I survive this?",
                    "lastran": 0
                },
                {
                    "peak": 20,
                    "msg": "*packs its bags, heads for the door*\nI'm not paid enough for this.",  # noqa E501
                    "lastran": 0
                }
            ],
        }
        return True

    def loadConfig(self) -> None:
        """ Load a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/typingReact.json'
        json_file = {}
        try:
            with open(file_, 'r') as load_file:
                json_file = json.load(load_file)
        except json.decoder.JSONDecodeError:
            logger.error('Config file empty or bad format. ', exc_info=True)
        except FileNotFoundError:
            logger.error(f'Config file not found: {file_}', exc_info=True)

        self.trConfig = json_file
        self.activeConfig = file_
        return

    def saveConfig(self) -> bool:
        """ Save a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/typingReact.json'
        path = pathlib.Path('/'.join(file_.split('/')[:-1]))
        path.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_, 'w') as save_file:
                save_file.write(json.dumps(self.trConfig, indent=4))
        except OSError:
            logger.error(f'File not be saved: {file_}', exc_info=True)
        return

    async def onMessage(self, **kwargs):
        """ TO DO: Few basic commands controlled by guild owner/allowed """
        pass

    async def onTyping(self, **kwargs):
        """ Hook to discord.on_typing event called from core script

        Uses the number of people typing to trigger a possible message from
        the bot back into the channel. Highest peak is used, cooldown is
        global for all actions.

        Keyword Args:
            channel(object): discord.channel object
            user(object): discord.user object
            when(datetime): When the event was triggered UTC
        """
        channel = kwargs.get('channel')
        user = kwargs.get('user')
        # when = kwargs.get('when')

        if self.lastin:
            logger.debug(f'Last in: {time.time() - self.lastin}')
        self.lastin = time.time()

        if channel.guild is None:
            return
        if channel.guild.id in self.trConfig['SYS-Rec']['optoutGuilds']:
            return
        logger.debug(f'Typing: {user.name}')

        self.checkGuild(str(channel.guild.id))
        self._cleanup()
        qsearch = [u for u in self.tracktyping
                   if u[0] == user.id and u[2] == channel.id]
        if not(qsearch):
            self.tracktyping.append(
                (user.id, round(time.time()), channel.id))

        cooldown = self.trConfig[str(channel.guild.id)].get('cooldown', 86400)
        channels = {}
        # Get unique channels with how many active typing
        # This is such a hack.  I love it. <3
        # It was also at this point in my life I learned GiGi = Wild
        for tt in self.tracktyping:
            channels[tt[2]] = channels.get(tt[2], 0) + 1

        logger.debug(f'Channels: {channels}')
        for pile in self.trConfig[str(channel.guild.id)].get('piles', []):
            for ch in channels:
                if channels[ch] >= pile.get('peak', 999):
                    elap = time.time() - pile.get('lastran', 0)
                    if elap > cooldown:
                        pile['lastran'] = round(time.time())
                        # Is it safe to assume that the person who typed
                        # and triggered this is in the guild/channel we
                        # care about?  I think it is.
                        deets = (channel.guild.id, channel.id, channel.name,
                                 user.id, user.name, pile.get('msg', ''))
                        logging.info(f'Reacting to a lot of typing: {deets}')
                        await channel.send(pile.get('msg', ''))
        return

    def _cleanup(self):
        """ Cleans up what we are tracking if older than 9 seconds"""
        newlist = []
        for user in self.tracktyping:
            uid, tic, channel = user
            if round(time.time()) - tic > 9:
                continue
            newlist.append((uid, tic, channel))
        self.tracktyping = newlist
        return

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
