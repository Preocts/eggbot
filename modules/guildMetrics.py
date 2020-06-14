""" Collect and process select metrics of a guild

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    Don't worry, this is mostly harmeless
"""
import logging
import time
from utils import jsonIO

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return guildMetrics()


class guildMetrics:
    """ Defines the guildMetrics class """

    name = "guildMetrics"
    allowReload = False
    instCount = 0

    def __init__(self, inFile: str = "./config/guildMetrics.json"):
        logger.info(f'Initialize guildMetrics: {inFile}')
        self.gmConfig = {}
        self.activeConfig = None
        self.saveRate = 60
        self.lastSave = time.time()
        self.loadConfig(inFile)
        guildMetrics.instCount += 1
        logger.info(f'Config loaded with {len(self.gmConfig)} records.')
        return

    def __str__(self):
        return str(self.gmConfig)

    def __bool__(self):
        if len(self.gmConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        if self.activeConfig is None:
            logger.warn('Lost activeConfig name while closing, not good.')
            logger.info('Dump file attempt: ./config/guildMetrics_DUMP.json')
            self.activeConfig = "./config/guildMetrics_DUMP.json"
        self.saveConfig(self.activeConfig)
        guildMetrics.instCount -= 1
        return

    def checkSys(self) -> bool:
        """ Creates a system record if it does not exist in the config """
        if "SYS-Rec" in self.gmConfig.keys():
            return True
        sysSchema = {
            'optoutGuilds': [],
            'optoutUsers': []
        }
        self.gmConfig["SYS-Rec"] = sysSchema
        self.gmConfig["guilds"] = {}
        return True

    def checkGuild(self, guildID: str, guildName: str) -> bool:
        """ Creates a guild if it does not exist in the config """
        if guildID in self.gmConfig["guilds"].keys():
            return True
        guildSchema = {
            'guildNames': [guildName, ],
            'entryMade': time.strftime('%j|%Y-%m-%d|%H.%M.%S|%z'),
            'members': {}
        }
        self.gmConfig["guilds"][guildID] = guildSchema
        return True

    def checkUser(self, guildID: str, userID: str, userName: str) -> bool:
        """ Creates a user entry in guild if it does not exist in the config"""
        if userID in self.gmConfig["guilds"][guildID]["members"].keys():
            return True
        hours = [0] * 24
        userSchema = {
            'userNames': [userName, ],
            'userNicks': [],
            'entryMade': time.strftime('%j|%Y-%m-%d|%H.%M.%S|%z'),
            'messageCounters': [0, 0, 0],
            'lastSeen': time.strftime('%j|%Y-%m-%d|%H.%M.%S|%z'),
            'hours': hours
        }
        self.gmConfig["guilds"][guildID]["members"][userID] = userSchema
        return True

    def logit(self, guildID: str, guildName: str, userID: str,
              userName: str, userNick: str, content: str) -> bool:
        """ Processes a messasge and stores all the data for the Egg

            *insert big-brother references here*
        """
        self.checkSys()
        if guildID in self.gmConfig["SYS-Rec"]["optoutGuilds"]:
            logger.debug(f'{guildID} is on the optout list')
            return False
        if userID in self.gmConfig["SYS-Rec"]["optoutUsers"]:
            logger.debug(f'{userID} is on the output list')
            return False
        self.checkGuild(guildID, guildName)
        self.checkUser(guildID, userID, userName)
        user = self.gmConfig["guilds"][guildID]["members"][userID]
        nowTime = time.strftime('%j|%Y-%m-%d|%H.%M.%S|%z')
        if not(userName in user["userNames"]):
            user["userNames"].append(userName)
        if not(userNick in user["userNicks"]):
            user["userNicks"].append(userNick)
        user["lastSeen"] = nowTime
        user["hours"][int(time.strftime('%H'))] += 1
        user["messageCounters"][0] += 1
        user["messageCounters"][1] += len(content.split(' '))
        if len(content):
            if content[-1] == ".":
                user["messageCounters"][2] += 1
        self.gmConfig["guilds"][guildID]["members"][userID] = user
        if (time.time() - self.lastSave) >= self.saveRate:
            self.lastSave = time.time()
            self.saveConfig(self.activeConfig)
        return True

    def loadConfig(self, inFile: str = "./config/guildMetrics.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.gmConfig = jsonIO.loadConfig(inFile)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {"status": False, "response": "Error loading config"}
        self.activeConfig = inFile
        logger.debug(f'loadConfig success: {inFile}')
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/guildMetrics.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            jsonIO.saveConfig(self.gmConfig, outFile, raw=False)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'saveConfig success: {outFile}')
        return {"status": True, "response": "Config saved"}

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

        if chtype != "text":
            return True

        # The egg watches. The egg knows.
        self.logit(str(message.guild.id), message.guild.name,
                   str(message.author.id), message.author.name,
                   message.author.display_name, message.clean_content)
        return True

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
