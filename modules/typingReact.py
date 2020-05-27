""" Fun things that happen when everyone gets involved

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    #BlameNay
"""
import logging
import time
from . import jsonIO

logger = logging.getLogger("default")  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return typingReact()


class typingReact:
    """ Defines the typingReact class """

    name = "typingReact"
    allowReload = True
    instCount = 0

    def __init__(self, inFile: str = "./config/typingReact.json"):
        logger.info(f'Initialize typingReact: {inFile}')
        self.trConfig = {}
        self.activeConfig = None
        self.tracktyping = []
        self.loadConfig(inFile)
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
        if self.activeConfig is None:
            logger.warn('Lost activeConfig name while closing, not good.')
            logger.info('Dump file attempt: ./config/typingReact_DUMP.json')
            self.activeConfig = "./config/typingReact_DUMP.json"
        self.saveConfig(self.activeConfig)
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

    def loadConfig(self, inFile: str = "./config/typingReact.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.trConfig = jsonIO.loadConfig(inFile)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {"status": False, "response": "Error loading config"}
        self.activeConfig = inFile
        logger.debug(f'loadConfig success: {inFile}')
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/typingReact.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            jsonIO.saveConfig(self.trConfig, outFile, raw=False)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'saveConfig success: {outFile}')
        return {"status": True, "response": "Config saved"}

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

        if channel.guild is None:
            return

        self.checkGuild(str(channel.guild.id))
        self._cleanup()
        qsearch = [u for u in self.tracktyping if u[0] == user.id]
        if not(len(qsearch)):
            self.tracktyping.append((user.id, round(time.time())))

        outmsg = None
        cooldown = self.trConfig[str(channel.guild.id)].get('cooldown', 86400)
        for pile in self.trConfig[str(channel.guild.id)].get('piles', []):
            if len(self.tracktyping) >= pile.get('peak'):
                elap = time.time() - pile.get('lastran', 0)
                if elap > cooldown:
                    outmsg = pile.get('msg')
                    pile['lastran'] = round(time.time())
        if outmsg is not None:
            # await channel.send(outmsg)
            print(''.join(['#'] * 70))
            print(outmsg)
            print(''.join(['#'] * 70))
        # ADD CHECK COOLDOWN AND UPDATE LASTRAN
        return

    def _cleanup(self):
        """ Cleans up what we are tracking if older than 3 seconds"""
        newlist = []
        for user in self.tracktyping:
            uid, tic = user
            if round(time.time()) - tic > 3:
                continue
            newlist.append((uid, tic))
        self.tracktyping = newlist


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
