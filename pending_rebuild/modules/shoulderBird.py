"""
    ShoulderBird is tool that add DM pings on keyword from chat

    Alerts a user when a keyword of their choice is said in any chat
    that is being watched by the bot. The keywords are scanned by regex
    with the messege's content being relayed to the user via a DM from
    the bot when the regex finds a match.

    Created by Preocts
        Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot
"""

import re
import json
import logging
import pathlib
from eggbot.utils import eggUtils

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return shoulderBird()


class shoulderBird:
    """ ShoulderBird scans incomming discord.onmessage events for keywords

    Keywords are defined from the configuration file loaded on the
    initialization of a class instance. Guilds and users are stored by
    their ID in string form.

    This class was designed to work inline with Discord.py library but only
    uses the library through arguments passed in the method onMessage().

    Class Attributes:
        name [str] : Name of class
        version [str] : Version of module release
        allowReload [bool] : Flag for external use. If ture this module is
            save to reload the config at anytime during use without risk
            of data loss.
        instCount [int] : Increment counter of how many instances are declared

    Attributes:
        sbConfig [dict] : Stores the instances copy of the configuration
        activeConfig [str] : Path and filename of the loaded configuration
    """

    name = "shoulderBird"
    version = "v1.0.0"
    allowReload = True
    instCount = 0

    # ╔════════════*.·:·.✧    ✦    ✧.·:·.*════════════╗
    #            Standard Eggbot module setup
    # ╚════════════*.·:·.✧    ✦    ✧.·:·.*════════════╝
    def __init__(self):
        """INIT"""
        logging.info('Start: Initializing shoulderBird')
        self.sbConfig = {}
        self.activeConfig = ""
        self.loadConfig()
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
        self.saveConfig()
        shoulderBird.instCount -= 1
        return

    def loadConfig(self) -> None:
        """ Load a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/shoulderBird.json'
        json_file = {}
        try:
            with open(file_, 'r') as load_file:
                json_file = json.load(load_file)
        except json.decoder.JSONDecodeError:
            logger.error('Config file empty or bad format. ', exc_info=True)
        except FileNotFoundError:
            logger.error(f'Config file not found: {file_}', exc_info=True)

        self.sbConfig = json_file
        self.activeConfig = file_
        return

    def saveConfig(self) -> bool:
        """ Save a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/shoulderBird.json'
        path = pathlib.Path('/'.join(file_.split('/')[:-1]))
        path.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_, 'w') as save_file:
                save_file.write(json.dumps(self.sbConfig, indent=4))
        except OSError:
            logger.error(f'File not be saved: {file_}', exc_info=True)
        return

    # ╔════════════*.·:·.✧    ✦    ✧.·:·.*════════════╗
    #           Shoulderbird internal methods
    # ╚════════════*.·:·.✧    ✦    ✧.·:·.*════════════╝
    def configCheck(self, guild: str, user: str):
        """ Ensures the config is healthy """
        logger.debug(f'[START] configCheck : {guild}, {user}')
        if not(isinstance(self.sbConfig, dict)):
            self.sbConfig = {}
        if not(guild in self.sbConfig):
            self.sbConfig[guild] = {}
        if not(user in self.sbConfig[guild]):
            self.sbConfig[guild][user] = {
                "regex": "",
                "toggle": True,
                "ignore": [],
                "reminder": 0
            }
        self.saveConfig()
        logger.debug('[FINISH] configCheck : ')
        return

    def getBirds(self, guild: str) -> dict:
        """ Fetch all defined Birds from the config file

        Args:
            [str] : Guild ID to pull results from

        Returns:
            [dict] : {"status": [bool], "response": [str]}
        """
        logger.debug(f'[START] getBirds : {guild}')
        if ((guild in self.sbConfig) and len(self.sbConfig[guild])):
            logger.debug(f'[FINISH] getBirds : {len(self.sbConfig[guild])}')
            return {"status": True, "response": self.sbConfig[guild]}
        logger.debug('[FINISH] getBirds : Guild not found or empty')
        return {"status": False, "response": "Guild not found or empty"}

    def getBird(self, guild: str, user: str) -> dict:
        """ Fetch a single defined Bird from the config file

        Args:
            [str] : Guild ID to pull results from
            [str] : User ID to pull results for

        Returns:
            [dict] : {"status": [bool], "response": [str]}
        """
        logger.debug(f'[START] getBird : {guild}, {user}')
        response = None
        if ((guild in self.sbConfig) and len(self.sbConfig[guild])):
            if user in self.sbConfig[guild]:
                response = (self.sbConfig[guild][user]["regex"],
                            self.sbConfig[guild][user]["toggle"])
                logger.debug(f'[FINISH] getBird : {response}')
                return {"status": True, "response": response}
        logger.debug('[FINISH] getBird : Guild or user not found')
        return {"status": False, "response": "Guild or user not found"}

    def listBirds(self, user) -> dict:
        """ List all of the birds a user has set

        Args:
            [str] : User ID to pull results for

        Returns:
            [dict] : {'status': [bool], 'response': [list]}
        """
        logger.debug(f'[START] listBirds : {user}')
        birdlist = []
        for guild, values in self.sbConfig.items():
            if user in values:
                birdlist.append([guild, self.sbConfig[guild][user]['regex']])
        logger.debug(f'[FINISH] listBirds : {len(birdlist)}')
        if birdlist:
            return {'status': True, 'response': birdlist}
        return {'status': False, 'response': 'No birds found.'}

    def putBird(self, guild, message) -> dict:
        """ Stores a Bird into the loaded config

        Args:
            [str] : Discord Guild ID
            [discord.message] : Discord message

        Returns:
            [dict] : {'status': [bool], 'response': [str]}
        """
        logger.debug(f'[START] putBird : {message.clean_content}')
        user = str(message.author.id)
        # messsage format : "sb!set [guild] = [regex]"
        regex = message.clean_content.split('=')[1:][0].strip()  # Just [regex]

        self.configCheck(guild, user)
        self.sbConfig[guild][user]['regex'] = regex
        logger.debug('[FINISH] putBird : ')
        return {'status': True, 'response': 'Bird has been stored in config'}

    def delBird(self, user: str) -> dict:
        """ Removes users Birds from the loaded config (no undo)

        Args:
            [str] : User ID to delete

        Returns:
            [dict] : {"status": [bool], "response": [str]}
        """
        logger.debug(f'[START] delBird : {user}')
        response = None
        for guild, values in self.sbConfig.items():
            if user in values:
                del self.sbConfig[guild][user]
                response = "Birds have been deleted"
        logger.debug(f'[FINISH] delBird : {response}')
        if response is None:
            return {"status": False, "response": "No birds were found"}
        return {"status": True, "response": "Birds have been deleted"}

    def toggleBird(self, user: str, state: bool) -> dict:
        """ Toggles ShoulderBird in all guilds for a user to given bool

        This used to be an actual toggle, maybe one day it will be again. For
        brevity, sb!toggle was replaced with sb!on and sb!off in v1.0.0.

        Args:
            [str] : User ID to toggle
            [bool] : Target state of user's birds

        Returns:
            [dict] : {"status": [bool], "response": [str]}
        """
        logger.debug(f'[START] toggleBird : {user}, {state}')

        for guild, values in self.sbConfig.items():
            if user in values:
                self.sbConfig[guild][user]['toggle'] = state
        if state:
            response = 'Birds now active for all guilds'
        else:
            response = 'Birds now inactive for all guilds'
        logger.debug(f'[FINISH] toggleBird : {response}')
        return {'status': True, 'response': response}

    def birdCall(self, guild: str, user: str, message: str) -> dict:
        """ Uses regEx to find defined keywords in a chat message

        Args:
            [str] : Guild ID to pull results from
            [str] : User ID to pull results for
            [str] : Message content to run regex against

        Returns:
            [dict] : {"status": [bool], "response": [list]}
        """
        logger.debug(f'[START] birdCall : {guild}, {user}, {message}')
        # Is the guild configured?
        results = self.getBirds(guild)
        if not(results["status"]):
            logger.debug('[FINISH] birdCall : Guild returned no results: '
                         f'{guild}')
            return {"status": False, "Response": []}
        nest = results["response"]
        birdList = []
        for bird in nest:
            # check all available active regex for a hit
            if nest[bird]["toggle"]:
                if user in nest[bird]["ignore"]:
                    continue
                rx = nest[bird]["regex"]
                if not(len(rx)):  # Catch for empty regex
                    continue
                findRg = re.compile(r'\b{}\b'.format(rx), re.I)
                found = findRg.search(message)
                if found:
                    logger.info(f'Bird found for {bird}')
                    try:
                        birdList.append(int(bird))
                    except ValueError as e:
                        logger.warning(f'Bad bird: {guild}, {user}, {e}')
                        continue
        if len(birdList):
            logger.debug(f'[FINISH] birdCall : {birdList}')
            return {"status": True, "response": birdList}
        logger.debug('[FINISH] birdCall : No results')
        return {"status": False, "repsonse": []}

    def gagBird(self, user: str, target: str) -> dict:
        """ Toggles a given target for a given guild to be ignored

        While logging messages may capture messages from ignored users if
        the logging levels are set low enough, ignored users will not trigger
        a shoulderBird alert.

        Hopefully, someday, Discord figures out the simple application of
        display: none; to hide blocked users in the channel history. >:V

        Args:
            [str] : User ID to assign config to
            [str] : User ID to ignore

        Returns:
            [dict] : {"status": [bool], "response": [str]}
        """
        logger.debug(f'[START] gagBird : {user}, {target}')
        response = None
        for guild, values in self.sbConfig.items():
            if user in values:
                # Unignore
                if target in self.sbConfig[guild][user]['ignore']:
                    idx = self.sbConfig[guild][user]['ignore'].index(target)
                    self.sbConfig[guild][user]['ignore'].pop(idx)
                    response = "User is no longer ignored in all guilds"
                    continue
                self.sbConfig[guild][user]['ignore'].append(target)
                response = "User is now ignored in all guilds"
        logger.debug(f'[FINSIH] gagBird : {response}')
        if response is None:
            return {'status': False, 'response': 'You have no birds to edit'}
        return {'status': True, 'response': response}

    # ╔════════════*.·:·.✧    ✦    ✧.·:·.*════════════╗
    #              Discord.py hook methods
    # ╚════════════*.·:·.✧    ✦    ✧.·:·.*════════════╝
    async def onMessage(self, **kwargs) -> bool:
        """ Hook method to be called from core script on Message event

        Keyword Args:
            message [discord.message] : a discord.message class
            client [discord.client] : Active discord client reference

        Returns:
            None
        """
        logger.debug('[START] onMessage : ')
        Supported_Channels = (
            "<class 'discord.channel.DMChannel'>",
            "<class 'discord.channel.TextChannel'>")
        message = kwargs.get('message')
        client = kwargs.get('client')

        if client is None:
            return

        if str(type(message.channel)) not in Supported_Channels:
            logger.debug('[FINISH] onMessage : Channel type not support')
            return

        # DM Channel catch
        if str(type(message.channel)) == Supported_Channels[0]:  # DM channel
            # Special case !help command
            if message.clean_content.lower() == "!help":
                response = 'ShoudlerBird installed: **sb!help** for details'
                await message.author.dm_channel.send(response)
                return

            # Process possible ShoulderBird Commands
            if message.clean_content[0:3].lower() == "sb!":
                response = self.commands(message, kwargs["client"])
                if response:
                    await message.author.dm_channel.send(response)
                return
            return

        # ╔════════════*.·:·.✧    ✦    ✧.·:·.*════════════╗
        #  ShoulderBird - Alerting for custom search strings
        # ╚════════════*.·:·.✧    ✦    ✧.·:·.*════════════╝
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

                logger.debug(f'Anti-snoop: {feathers} - {snack}')
                if bird and snack:
                    await bird.create_dm()
                    msg = ''.join([
                        'Mention alert: **',
                        str(message.author.display_name),
                        '** mentioned you in **',
                        message.channel.name,
                        '** saying:\n`',
                        message.clean_content,
                        '`'])
                    await bird.dm_channel.send(msg)
        logging.debug('[FINISH] onMessage : ')
        return

    def commands(self, message, dClient) -> str:
        """ Process any DM commands sent """

        # strip the !trigger word and leading space out of the message
        cmdTrig = message.clean_content.split(' ')[0].lower()

        if cmdTrig == 'sb!set':
            # sb!set [guild] = [body]
            if '=' not in message.clean_content:
                return 'Error: Formatting incorrect. \n' \
                       '```sb!set [Guild Name or ID] = [regular expression]```'
            # We need to pull the [guild] provided and do two things,
            # 1) Confirm bot is in that guild
            # 2) Ensure we are using a guild.id and not a name
            cmdTarg = message.clean_content.split('=')[0].strip(cmdTrig).strip()  # noqa
            guildID = None
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
                return f'Error: I\'m not that guild: {cmdTarg}'

            result = self.putBird(guildID, message)
            self.saveConfig()
            return result['response']

        if cmdTrig == 'sb!on':
            # Turn on all birds for user
            result = self.toggleBird(str(message.author.id), True)
            self.saveConfig()
            return result['response']

        if cmdTrig == 'sb!off':
            # Turn on all birds for user
            result = self.toggleBird(str(message.author.id), False)
            self.saveConfig()
            return result['response']

        if cmdTrig == 'sb!ignore':
            # sb!ignore [name/ID]
            # Confirm if the name/ID is in the guild provided
            cmdBody = message.clean_content.split()[1:][0]
            if not(cmdBody):
                return 'Error: Formatting incorrect. \n' \
                       '```sb!ignore [username or ID to ignore]```'

            # Find this user ID if available
            # TODO: This will need some improvements for speed
            targID = None
            for user in dClient.users:
                # Provided a user ID
                if eggUtils.isInt(cmdBody) and user.id == int(cmdBody):
                    targID = str(user.id)
                    break
                # Provided a user Name
                if not(eggUtils.isInt(cmdBody)) and user.name == cmdBody:
                    targID = str(user.id)
                    break
            if targID is None:
                return f'Error: Can\'t find {cmdBody}. Be sure you are ' \
                        'providing either their Username without the #0000 ' \
                        'or their user ID.'
            result = self.gagBird(str(message.author.id), targID)
            self.saveConfig()
            return result['response']

        if cmdTrig == 'sb!delete':
            # sb!remove
            result = self.delBird(str(message.author.id))
            self.saveConfig()
            return result['response']

        if cmdTrig == 'sb!list':
            # sb!list
            result = self.listBirds(str(message.author.id))
            if result['status']:
                dmmessage = ['List of birds:\n```\n']
                for bird in result['response']:
                    guild = dClient.get_guild(int(bird[0]))
                    guild = guild.name if guild is not None else 'Unknown'
                    dmmessage.append(f'{guild} : {bird[1]}\n')
                dmmessage.append('```')
                return ''.join(dmmessage)
            else:
                return result['response']

        if cmdTrig == 'sb!help':
            # sb!help
            response = 'Command List: *There is no undo button!*\n```' \
                       '+ sb!list [guild name/ID]\n' \
                       '\tLists stored searches from all guilds\n' \
                       '+ sb!on\n' \
                       '\tTurns ShouldBird on for all guilds you have\n' \
                       '+ sb!off\n' \
                       '\tTurns ShouldBird off for all guilds you have\n' \
                       '+ sb!set [guild name or ID] = [RegEx]\n' \
                       '\tSets a user\'s RegEx search for given guild\n' \
                       '\tguild name is case sensitive. If you have dev\n' \
                       '\tmode on you can provide the guild ID\n' \
                       '+ sb!ignore [user name (not nickname) or ID]\n' \
                       '\tToggles a user to be ignored by ShoulderBird\n' \
                       '\tacross all guilds you have a search in. If they\n' \
                       '\tare already ignored, they will be unignored\n' \
                       '\tUser name excludes the #0000 numbers\n' \
                       '+ sb!delete\n' \
                       '\tDeletes all your birds. ***There is no undo!***\n' \
                       '+ sb!help\n' \
                       '\tDisplays this help box\n```'
            return response

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
