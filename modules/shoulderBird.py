"""
    ShoulderBird is a Discord channel alert tool

    Alerts a user when a keyword of their choice is said in any chat
    that is being watched by the bot.

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

    Common Use Examples:
    ---
    Initialize: (loads config)
        SB = shoulderBird.shoulderBird("FileNameOptional")

    Create/Update a search:
        results = SB.putBird("guild", "user", "RegEx Search String")

    Add/Remove ignore name:
        results = SB.gagBird("guild", "user")

    Delete a search:
        results = SB.delBird("guild", "user")

    Toggle a search on/off (returns new state):
        results = SB.toggleBird("guild", "user")

    Scan a message for a matching search:
        results = SB.birdCall("guild", "user", "Message String")
        # If results["status"] is True then results["response"] will be
        # the user of who had a matching search.

    Save Config:
        SB.saveConfig("FileNameOptional")
"""
import logging
from utils import eggUtils
import re
from . import jsonIO

logger = logging.getLogger("default")  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return shoulderBird()


class shoulderBird:
    """
    Defines the ShouldBird Object

    Config format:
    {
        "guild" {
            "user": {
                "regex": "Expression",
                "toggle": Boolean,
                "ignore": ["string",]
            }
        }
    }

    Definitions:
        Bird : A single search string in regEx
    """

    name = "shoulderBird"
    allowReload = True
    instCount = 0

    def __init__(self, inFile: str = "./config/shoulderBird.json"):
        """INIT"""
        logging.info(f'Start: Initializing shoulderBird: {inFile}')
        self.sbConfig = {}
        self.activeConfig = ""
        self.loadConfig(inFile)
        shoulderBird.instCount += 1
        logger.info(f'Config loaded with {len(self.sbConfig)}')
        return

    def __str__(self):
        return str(self.sbConfig)

    def __bool__(self):
        if len(self.sbConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        if self.activeConfig is None:
            logger.warn('Lost activeConfig name while closing, not good.')
            logger.info('Dump file attempt: ./config/shoulderBird_DUMP.json')
            self.activeConfig = "./config/shoulderBird_DUMP.json"
        self.saveConfig(self.activeConfig)
        shoulderBird.instCount -= 1
        return

    def getBirds(self, guild: str) -> dict:
        """
        Fetch all defined Birds from the config file

        Args:
            guild (str): Guild ID to pull results from

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'getBirds: {guild}')
        if ((guild in self.sbConfig) and
           len(self.sbConfig[guild])):
            return {"status": True, "response": self.sbConfig[guild]}
        return {"status": False, "response": "Guild not found or empty"}

    def getBird(self, guild: str, user: str) -> dict:
        """
        Fetch a single defined Bird from the config file

        Args:
            guild (str): Guild ID to pull results from
            user (str): User ID to pull results for

        Returns:
            (dict) : {"status": bool, "response": (str, bool)}

        Raises:
            None
        """

        logger.debug(f'getBird call: {guild} | {user}')
        response = None
        if ((guild in self.sbConfig) and
           len(self.sbConfig[guild])):
            if user in self.sbConfig[guild]:
                response = (self.sbConfig[guild][user]["regex"],
                            self.sbConfig[guild][user]["toggle"])
                return {"status": True, "response": response}
        return {"status": False, "response": "Guild or user not found"}

    def putBird(self, guild: str, user: str, regex: str) -> dict:
        """
        Stores a Bird into the loaded config

        Args:
            guild (str): Guild ID to assign
            user (str): User ID to assign
            regex (str): Regex expression to search chat with
                         All expressions are word-bound be default and
                         case insensitive

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'putBird: {guild} | {user} | {regex}')
        if not(guild in self.sbConfig):
            self.sbConfig[guild] = {}
        self.sbConfig[guild][user] = {}
        self.sbConfig[guild][user]["regex"] = regex
        self.sbConfig[guild][user]["toggle"] = True
        self.sbConfig[guild][user]["ignore"] = []
        return {"status": True, "response": "Bird put in config"}

    def delBird(self, guild: str, user: str) -> dict:
        """
        Removes a Bird from the loaded config

        Args:
            guild (str): Guild ID
            user (str): User ID to delete

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'delBirds: {guild} | {user}')
        if guild in self.sbConfig:
            if user in self.sbConfig[guild]:
                del self.sbConfig[guild][user]
                return {"status": True, "response": "Bird deleted"}
        return {"status": False, "response": "Guild or user not found"}

    def toggleBird(self, guild: str, user: str) -> dict:
        """
        Toggles ShoulderBird for a specific guild

        Args:
            guild (str): Guild ID
            user (str): User ID to toggle

        Returns:
            (dict) : {"status": bool, "response": str}

        Raises:
            None
        """

        logger.debug(f'delBirds: {guild} | {user}')
        response = None
        if guild in self.sbConfig:
            if user in self.sbConfig[guild]:
                curToggle = self.sbConfig[guild][user]["toggle"]
                if curToggle:
                    curToggle = False
                    response = f'Bird now inactive for requested guild.'
                else:
                    curToggle = True
                    response = f'Bird now active for requested guild.'
                self.sbConfig[guild][user]["toggle"] = curToggle
        return {"status": curToggle, "response": response}

    def birdCall(self, guild: str, user: str, message: str) -> dict:
        """
        Uses regEx to find defined keywords in a chat message

        Args:
            guild (str): Guild ID to pull results from
            user (str): User ID to pull results for
            message (str): Message content to run regex against

        Returns:
            (dict) : {"status": bool, "response": (list)[UserIDs]}

        Raises:
            None
        """

        logger.debug(f'Bird Call: {guild} | {user} | {message}')
        # Is the guild configured?
        results = self.getBirds(guild)
        if not(results["status"]):
            logger.debug(f'Guild returned no results: {guild}')
            return {"status": False, "Response": []}
        nest = results["response"]
        birdList = []
        for bird in nest:
            # check all available active regex for a hit
            if nest[bird]["toggle"]:
                if user in nest[bird]["ignore"]:
                    continue
                rx = nest[bird]["regex"]
                findRg = re.compile(r'\b{}\b'.format(rx), re.I)
                found = findRg.search(message)
                if found:
                    logger.info(f'Bird found for {bird}')
                    try:
                        birdList.append(int(bird))
                    except ValueError as e:
                        logger.warning(f'Bad bird: {guild} | {user} | {e}')
                        continue
        if len(birdList):
            return {"status": True, "response": birdList}
        logger.info('Empty Nest')
        return {"status": False, "repsonse": []}

    def gagBird(self, guild: str, user: str, target: str) -> dict:
        """
        Toggles a given target for a given guild to be ignored

        While logging messages may capture messages from ignored users if
        the logging levels are set low enough, ignored users will not trigger
        a shoulderBird alert.

        Hopefully, someday, Discord figures out the simple application of
        display: none; to hide blocked users in the channel history. >:V

        Args:
            guild (str): Guild ID
            user (str): User ID to assign config to
            target (str): User ID to ignore

        Returns:
            {"status": True/False, "response": "string"}

        Raises:
            None
        """

        logger.debug(f'Gag Bird: {guild} | {user}')
        if not(guild in self.sbConfig):
            return {"status": False, "response": "No nests in that guild"}
        if not(user in self.sbConfig[guild]):
            return {"status": False, "response": "No bird by that user"}
        if target in self.sbConfig[guild][user]["ignore"]:
            ix = self.sbConfig[guild][user]["ignore"].index(target)
            self.sbConfig[guild][user]["ignore"].pop(ix)
            logger.debug(f'Bird listening: {target}')
            return {"status": True,
                    "response": f"Will listen to that person now."}
        else:
            self.sbConfig[guild][user]["ignore"].append(target)
            logger.debug(f'Bird ignoring: {target}')
            return {"status": True,
                    "response": "Will ignore that person now."}

    def loadConfig(self, inFile: str = "./config/shoulderBird.json") -> bool:
        """ Load a config into the class """

        logger.debug(f'loadConfig: {inFile}')
        try:
            self.sbConfig = jsonIO.loadConfig(inFile)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
            return {"status": False, "response": "Error loading config"}
        self.activeConfig = inFile
        logger.debug(f'loadConfig success: {inFile}')
        return {"status": True, "response": "Config Loaded"}

    def saveConfig(self, outFile: str = "./config/shoulderBird.json") -> bool:
        """ Save a config into the class """

        logger.debug(f'saveConfig: {outFile}')
        try:
            jsonIO.saveConfig(self.sbConfig, outFile)
        except jsonIO.JSON_Config_Error:
            logger.error('Failed loading config file!', exc_info=True)
        logger.debug(f'saveConfig success: {outFile}')
        return {"status": True, "response": "Config saved"}

    async def onMessage(self, chtype, message, **kwargs) -> bool:
        """
        Hook method to be called from core script on Message event

        Return value controls if additional mod calls are performed. If True
        the core script should continue with calls. If False the core script
        should break from iterations.

        Args:
            chtype (str) : Channel type. Either "text" or "dm" or "group"
            member (discord.member) : a discord.message class
            **kwargs :
                client (discord.client) : Active discord client reference

        Returns:
            (boolean)

        Raises:
            None
        """
        if not("client" in kwargs.keys()):
            return True

        if chtype == "dm":
            # Special case !help command
            if message.clean_content == "!help":
                response = 'ShoudlerBird installed: **sb!help** for details'
                await message.author.dm_channel.send(response)
                return True
            # Process possible ShoulderBird Commands
            if message.clean_content[0:3] == "sb!":
                response = self.commands(message, kwargs["client"])
                if response:
                    await message.author.dm_channel.send(response)
            return True

        # ShoulderBird Block - Alerting for custom search strings
        results = self.birdCall(str(message.guild.id), str(message.author.id),
                                message.clean_content)
        if results["status"]:
            birds = results["response"]
            for feathers in birds:
                bird = message.guild.get_member(feathers)
                # Anti-snooping: Stop bird chirping if user isn't in channel
                # This might need to be more efficient in the future
                for m in message.channel.members:
                    if m.id == feathers:
                        snack = m.id
                        break
                # snack = discord.utils.find(lambda m: m.id == feathers,
                #                            message.channel.members)

                logger.debug(f'Anti-snoop: {feathers} - {snack}')
                if bird and snack:
                    await bird.create_dm()
                    await bird.dm_channel.send('Mention alert: **' +
                                               str(message.author.display_name)
                                               + '** mentioned you in **' +
                                               message.channel.name +
                                               '** saying: \n`' +
                                               message.clean_content + '`')
        return True

    def commands(self, message, dClient) -> str:
        """ Process any DM commands sent """

        # strip the !trigger word and leading space out of the message
        cmdTrig = message.clean_content.split(' ')[0]
        cmdTarg = None
        cmdBody = None
        msg = message.clean_content.lstrip(cmdTrig).lstrip(' ')

        # If provided, next word in msg is always Guild Id/Name with
        # remaining being input delimted by '='. Split this here.
        msg = msg.split(' = ')
        if len(msg) >= 1:
            cmdTarg = msg[0]
        if len(msg) >= 2:
            cmdBody = msg[1]
        guildID = None
        # Confirm we are in the provided guild and get the ID
        for g in dClient.guilds:
            # Provided a guild ID
            if eggUtils.isInt(cmdTarg) and g.id == int(cmdTarg):
                guildID = str(g.id)
                break
            # Provided a guild Name
            if not(eggUtils.isInt(cmdTarg)) and g.name == cmdTarg:
                guildID = str(g.id)
                break
        if guildID is None and len(cmdTarg) != 0:
            return f'Error: I\'m not in guild: {cmdTarg}'

        # Set a bird up (regex string storage by guild and user)
        if cmdTrig == "sb!set":
            # sb!set [guild] = [body]
            if cmdBody is None:
                return 'Error: Formatting incorrect. \n' \
                       '```[Guild Name] = [regEx expression]```'
            self.putBird(guildID, str(message.author.id), cmdBody)
            self.saveConfig(self.activeConfig)
            return f'All set, new bird stored for {cmdTarg}'

        if cmdTrig == "sb!toggle":
            # sb!toggle [guild]
            result = self.toggleBird(guildID, str(message.author.id))
            self.saveConfig(self.activeConfig)
            return result["response"]

        if cmdTrig == "sb!ignore":
            # sb!ignore [guild] = [name/ID]
            # Confirm if the name/ID is in the guild provided
            if cmdBody is None:
                return 'Error: Formatting incorrect. \n' \
                       '```[Guild Name] = [name/ID to ignore]```'
            for u in dClient.get_guild(int(guildID)).members:
                # Provided a user ID
                targID = None
                if eggUtils.isInt(cmdBody) and u.id == int(cmdBody):
                    targID = str(u.id)
                    break
                # Provided a user Name
                if not(eggUtils.isInt(cmdBody)) and u.name == cmdBody:
                    targID = str(u.id)
                    break
            if targID is None:
                return f'Error: Can\'t find {cmdBody} in guild {cmdTarg}'
            result = self.gagBird(guildID, str(message.author.id), targID)
            self.saveConfig(self.activeConfig)
            return result["response"]

        if cmdTrig == "sb!remove":
            # sb!remove [guild]
            result = self.delBird(guildID, str(message.author.id))
            self.saveConfig(self.activeConfig)
            return result["response"]

        if cmdTrig == "sb!list":
            # sb!list [guild]
            result = self.getBird(guildID, str(message.author.id))
            if result["status"]:
                search = result["response"][0]
                toggle = result["response"][1]
                return f'RegEx: {search} | Toggle: {toggle}'
            else:
                return result["response"]

        if cmdTrig == "sb!help":
            # sb!help
            response = "Command List: *All names are case sensitive*\n```" \
                       "+ sb!set [guild name/ID] = [RegEx]\n" \
                       "\tSets a user's RegEx search for given guild\n" \
                       "+ sb!toggle [guild name/ID]\n" \
                       "\tToggles a search without deleting it\n" \
                       "+ sb!ignore [guild name/ID] = [name/ID]\n" \
                       "\tToggle a user to be ignored by ShoulderBird\n" \
                       "+ sb!remove [guild name/ID]\n" \
                       "\tDeletes a stored search from given guild\n" \
                       "+ sb!list [guild name/ID]\n" \
                       "\tLists stored search from given guild```"
            return response

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
