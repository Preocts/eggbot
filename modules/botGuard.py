"""
    botGuard only allows specific bots to join a guild

    When a bot joins the guild this module will check an allow list for
    the bot's ID. If not found the bot will be immediately kicked.

    A message will be posted to a selected channel telling members of the
    action, providing the bot's ID, and mentioning how to allow list
    a bot with that ID.

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot
"""

import logging
from utils import jsonIO

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return botGuard()


class botGuard:
    """
    Defines the BotGuard Object

    Config format:
    {
        "guild" {
            "active": (bool),
            "allowed": [ (int) IDs ],
            "channel": (int) ChannelID,
            "content": (str) "Message when a bot is kicked"
        }
    }
    """

    name = "botGuard"
    allowReload = True
    instCount = 0

    def __init__(self, inFile: str = "./config/botGuard.json"):
        """INIT"""
        logging.info(f'Start: Initializing botGuard: {inFile}')
        self.bgConfig = {}
        self.activeConfig = ""
        self.loadConfig(inFile)
        botGuard.instCount += 1
        logger.info(f'Config loaded with {len(self.bgConfig)}')
        return

    def __str__(self):
        return str(self.bgConfig)

    def __bool__(self):
        if len(self.bgConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        if self.activeConfig is None:
            logger.warn('Lost activeConfig name while closing, not good.')
            logger.info('Dump file attempt: ./config/botGuard_DUMP.json')
            self.activeConfig = "./config/botGuard_DUMP.json"
        self.saveConfig(self.activeConfig)
        botGuard.instCount -= 1
        return

    def loadConfig(self, inFile: str = "./config/botGuard.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.bgConfig = jsonIO.loadConfig(inFile)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {"status": False, "response": "Error loading config"}
        self.activeConfig = inFile
        logger.debug(f'loadConfig success: {inFile}')
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/botGuard.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            jsonIO.saveConfig(self.bgConfig, outFile)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'saveConfig success: {outFile}')
        return {"status": True, "response": "Config saved"}

    def addGuild(self, guild: str, active: bool = True) -> bool:
        """
        Adds a guild entry to the config. This will overwrite exiting values

        Args:
            guild (str): Guild ID to add
            active (boolean): If False the config will not be used.

        Returns:
            True

        Raises:
            None
        """
        logger.debug(f'Creating: {guild} | {active}')
        self.bgConfig[guild] = {
            "active": active,
            "allowed": [],
            "channel": 0,
            "content_deny": "",
            "content_allow": ""
        }
        return True

    def addAllow(self, guild: str, bot: str) -> dict:
        """
        Adds a bot ID to the list of allowed bots for a guild

        Args:
            guild (str): Guild ID to edit
            bot (str): User ID of the bot to allow

        Returns:
            dict : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'addAllow: {guild} | {bot}')
        try:
            int(bot)
        except ValueError:
            logger.warning(f'Incorrect ID Format provided: {bot}')
            return {"status": False, "response": "Incorrect ID format"}
        # Check if we already have this bot, pass gracefully
        if not(bot in self.bgConfig[guild]["allowed"]):
            self.bgConfig[guild]["allowed"].append(bot)
        return {"status": True, "response": "Bot added to allow list"}

    def removeAllow(self, guild: str, bot: str) -> dict:
        """
        Removes a bot ID to the list of allowed bots for a guild

        Args:
            guild (str): Guild ID to edit
            bot (str): User ID of the bot to remove

        Returns:
            dict : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'removeAllow: {guild} | {bot}')
        try:
            int(bot)
        except ValueError:
            logger.warning(f'Incorrect ID Format provided: {bot}')
            return {"status": False, "response": "Incorrect ID format"}
        # Check if we have this bot to remove, pass gracefully
        if bot in self.bgConfig[guild]["allowed"]:
            loc = self.bgConfig[guild]["allowed"].index(bot)
            self.bgConfig[guild]["allowed"].pop(loc)
        return {"status": True, "response": "Bot added to allow list"}

    def alertChannel(self, guild: str, channel: str) -> dict:
        """
        Sets the channel used to send alerts when another bot joins

        Args:
            guild (str): Guild ID to edit
            channel (str): Channel ID to sent message to

        Returns:
            dict : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'alertChannel: {guild} | {channel}')
        try:
            int(channel)
        except ValueError:
            logger.warning(f'Incorrect ID Format provided: {channel}')
            return {"status": False, "response": "Incorrect ID format"}
        self.bgConfig[guild]["channel"] = channel
        return {"status": True, "response": f"{channel} set for messages"}

    def denyMessage(self, guild: str, message: str) -> dict:
        """
        Sets the message displayed when a bot is kicked

        Empty messages are skipped. Use for "silent" operation

        Args:
            guild (str): Guild ID to edit
            message (str): Message to display on kick

        Returns:
            dict : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'denyMessage: {guild} | {message}')
        self.bgConfig[guild]["content_deny"] = message
        return {"status": True, "response": "Message set for Denied"}

    def allowMessage(self, guild: str, message: str) -> dict:
        """
        Sets the message displayed when a bot joins and is allowed

        Empty messages are skipped. Use for "silent" operation

        Args:
            guild (str): Guild ID to edit
            message (str): Message to display on join

        Returns:
            dict : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'allowMessage: {guild} | {message}')
        self.bgConfig[guild]["content_allow"] = message
        return {"status": True, "response": "Message set for Allowed"}

    def checkList(self, guild: str, bot: str) -> dict:
        """
        Checks the provided bot ID against allow list

        Return status will be False if the bot is not on the allow list. The
        remaining values in the returned dict will contain the channel any
        announcments are posted to and the content of that annoucement.

        If the guild is not configured or the guild is not active in the
        configutations then a True response will be passed and no actions
        will be taken.

        Args:
            guild (str): Guild ID to lookup
            bot (str): ID of the bot being checked

        Returns:
            dict : {"status": (bool), "channel": (int), "response": (str)}

        Raises:
            None
        """
        logger.debug(f'checkList: {guild} | {bot}')
        # Is the guild configured?
        if not(guild in self.bgConfig.keys()):
            # Create an inactive entry
            logger.info('Guild not setup in botGuard. Correcting...')
            self.addGuild(guild, False)
            return {"status": True, "channel": 0, "response": ""}

        # Is the guild active?
        if not(self.bgConfig[guild]["active"]):
            logger.info('Bot joined an inactive guild')
            return {"status": True, "channel": 0, "response": ""}

        # Is the bot allowed?
        if bot in self.bgConfig[guild]["allowed"]:
            # Yup. *notices your backstage pass* OwO
            logger.info('Bot was allowed to join')
            return {"status": True,
                    "channel": int(self.bgConfig[guild]["channel"]),
                    "response": self.bgConfig[guild]["content_allow"]}
        else:
            # Nope. owo ... I won't miss *pulls trigger*
            logger.warning('Bot joined that was not allowed.')
            return {"status": False,
                    "channel": int(self.bgConfig[guild]["channel"]),
                    "response": self.bgConfig[guild]["content_deny"]}

    async def onJoin(self, **kwargs) -> bool:
        """
        Hook method to be called from core script on Join event

        Keyword Args:
            member (discord.member): a discord.member class

        Returns:
            (boolean)

        Raises:
            None
        """
        member = kwargs.get('member')

        # Is this join a bot? Handle it *gun cocks*
        if not(member.bot):
            return True
        logger.info('Bot join detected...')
        bgResults = self.checkList(str(member.guild.id), str(member.id))
        if not(bgResults["status"]):
            # This bot is not allowed
            await member.kick(reason="This bot was not approved to join.")
            ch = member.guild.get_channel(bgResults["channel"])
            await ch.send(bgResults["response"])
            await ch.send('If this bot is desired, please add this '
                          f'ID to the allow list: {member.id}')
            return False
        else:
            # This bot is allowed
            ch = member.guild.get_channel(bgResults["channel"])
            await ch.send(bgResults["response"])
            await ch.send('If this bot was not desired, please remove '
                          f'this ID from the allow list: {member.id}')
            return True

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
