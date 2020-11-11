""" Collect and process select metrics of a guild

    Created by Preocts
        preocts@preocts.com | Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot

    Don't worry, this is mostly harmeless
"""
import json
import time
import logging
import pathlib
from eggbot.utils import eggUtils

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return guildMetrics()


class guildMetrics:
    """ Defines the guildMetrics class """

    name = "guildMetrics"
    allowReload = False
    instCount = 0

    def __init__(self):
        logger.info('Initialize guildMetrics')
        self.gmConfig = {}
        self.activeConfig = None
        self.saveRate = 60
        self.lastSave = time.time()
        self.loadConfig()
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
        self.saveConfig()
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
            self.saveConfig()
        return True

    def loadConfig(self) -> None:
        """ Load a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/guildMetrics.json'
        json_file = {}
        try:
            with open(file_, 'r') as load_file:
                json_file = json.load(load_file)
        except json.decoder.JSONDecodeError:
            logger.error('Config file empty or bad format. ', exc_info=True)
        except FileNotFoundError:
            logger.error(f'Config file not found: {file_}', exc_info=True)

        self.gmConfig = json_file
        self.activeConfig = file_
        return

    def saveConfig(self) -> bool:
        """ Save a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/guildMetrics.json'
        path = pathlib.Path('/'.join(file_.split('/')[:-1]))
        path.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_, 'w') as save_file:
                save_file.write(json.dumps(self.gmConfig, indent=4))
        except OSError:
            logger.error(f'File not be saved: {file_}', exc_info=True)
        return

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
