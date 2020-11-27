"""
    joinActions is a module for Egg_Bot for welcome messages

    Created by Preocts
        Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot

    Someone joins the guild, we might want to:
        - Assign a role to this lovely person
        - Check to see if this invite is tied to a specific role
          - Assign that role
        - Find active DM messages to send (by role)
          - Send them
        - Find active Chat messages to post (by role)
          - Post them

    So from the config we need an invite join table, welcome message,
    default role assignments, channel name, and active toggle
    We also want to set a welcome message, default role, invite roles,
    and toggle messages
"""
import json
import logging
import pathlib
from eggbot.utils import eggUtils

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return joinActions()


class joinActions:
    """ Defines the joinActions class """

    name = "joinActions"
    allowReload = True
    instCount = 0

    def __init__(self):
        """ Define __init__ """
        logger.info('Initialize joinActions')
        self.jaConfig = {}
        self.activeConfig = ''
        self.loadConfig()
        joinActions.instCount += 1
        logger.info(f'Config loaded with {len(self.jaConfig)}')
        return

    def __str__(self):
        return str(self.jaConfig)

    def __bool__(self):
        if len(self.jaConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self):
        """ Save configs on exit """
        self.saveConfig()
        joinActions.instCount -= 1
        return

    def create(self, guild: str, **kwargs) -> dict:
        """
        Creates a new join action in the configuration file

        Keyword arguements are optional, the config entry will be populated
        with empty values. .update() can be used to edit. Returns a failure
        if the "name" keyword already exists in the configuration file.

        Args:
            guild (int): discord.guild.id

        **kwargs:
            name (str): Unique name for the join action
            channel (str): Channel ID any message is displayed.
                           Leaving this blank will result in a direct message
            message (str): Displays this message to given channel/DM
            active (bool): Controls if the action is used or not

        Not currently used:
            addRole (str): Grants user a list of roles IDs on join
            limitRole (str): List roles IDs to recieve this join action
            limitInvite (str): List invite IDs to recieve this join action

        Returns:
            (dict) : {"status": true/false, "response": str}

        Raises:
            None
        """

        logger.debug(f'create: {guild} | {kwargs.items()}')
        try:
            guild = str(guild)
        except ValueError as err:
            return {"status": False, "response": err}
        # Default Config, change to add/remove:
        config = {'name': '',
                  'channel': '',
                  'roles': '',
                  'message': '',
                  'active': True,
                  'limitRole': '',
                  'limitInvite': ''}
        for key, value in kwargs.items():
            if key in config:
                config[key] = value
        if len(config["name"]) == 0:
            logger.debug('Name not provided for join action')
            return {"status": False, "response": "Name not defined"}
        if not(guild in self.jaConfig):
            self.jaConfig[guild] = [config, ]
        else:
            for n in self.jaConfig[guild]:
                if n["name"] == config["name"]:
                    logger.info(f'Name already exists: {config["name"]}')
                    return {"status": False, "response": "Name already exists"}
            self.jaConfig[guild].append(config)
        logger.debug(f'Join action added for {guild} | {config}')
        return {"status": True, "response": "Join action created"}

    def read(self, guild: str, name: str) -> dict:
        """
        Return a specific action for a guild

        Args:
            guild (str): ID of the guild
            name (str): Name of the join action being requested

        Returns:
            (dict) : {"status": true/false, "response": str}

        Raises:
            None
        """

        logger.debug(f'read: {guild} | {name}')
        if not(guild in self.jaConfig):
            logger.debug('Read: Guild not found')
            return {"status": False, "response": "Guild not found"}
        for n in self.jaConfig[guild]:
            if n["name"] == name:
                logger.debug('Read: Join action found')
                return {"status": True, "response": n}
        logger.debug('Read: Name not found')
        return {"status": False, "response": "Name not found"}

    def readAll(self, guild: str) -> dict:
        """
        Return all actions for a guild

        Args:
            guild (str): ID of the guild

        Returns:
            (dict) : {"status": true/false, "response": list}

        Raises:
            None
        """

        logger.debug(f'readAll: {guild}')
        if not(guild in self.jaConfig):
            logger.debug('readAll: Guild not found')
            return {"status": False, "response": "Guild not found"}
        return{"status": True, "response": self.jaConfig[guild]}

    def update(self, guild: str, name: str, **kwargs) -> dict:
        """
        Update an existing join action in the configuration file

        Keyword arguements are optional, the config entry will be populated
        with current values. Return a failure if the name keyword is not found.
        This cannot and will not rename a join action. "name" is ignored in
        the keywords.

        Args:
            guild (str): ID of the guild
            name (str): Name of the join action being updated
        **kwargs:
            See .create()

        Returns:
            (dict) : {"status": true/false, "response": str}

        Raises:
            None
        """

        logger.debug(f'Update: {guild} | {name} | {kwargs.items()}')
        results = self.read(guild, name)
        if not(results["status"]):
            return {"status": False, "response": "Guild or Name not found"}
        config = results["response"]
        for key, value in kwargs.items():
            if (key in config) and (key != 'name'):
                config[key] = value

        for action in self.jaConfig[guild]:
            if action["name"] == name:
                i = self.jaConfig[guild].index(action)
                logger.debug(f'Update: Updating join action index: {i}')
                self.jaConfig[guild][i] = config
                return {"status": True, "response": "Join action updated"}
        logger.warning('Something went wrong: name missing')
        return {"status": False, "response": "Something went wrong"}

    def delete(self, guild: str, name: str) -> dict:
        """
        Deletes a stored config for welcome messages

        Args:
            guild (str): ID of the guild
            name (str): Name of the join action being requested

        Returns:
            (dict) : {"status": true/false, "response": str}

        Raises:
            None
        """
        logger.debug(f'deleteMessage: {guild} | {name}')
        if not(guild in self.jaConfig):
            logger.debug('Delete: Guild not found')
            return {"status": False, "response": "Guild not found"}
        for n in self.jaConfig[guild]:
            if n["name"] == name:
                logger.debug(f'Deleting join action name: {name}')
                i = self.jaConfig[guild].index(n)
                del self.jaConfig[guild][i]
                return {"status": True, "response": "Join action deleted"}
        logger.debug('Delete: Name not found')
        return {"status": False, "response": "Join action name not found"}

    def loadConfig(self) -> None:
        """ Load a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/joinActions.json'
        json_file = {}
        try:
            with open(file_, 'r') as load_file:
                json_file = json.load(load_file)
        except json.decoder.JSONDecodeError:
            logger.error('Config file empty or bad format. ', exc_info=True)
        except FileNotFoundError:
            logger.error(f'Config file not found: {file_}', exc_info=True)

        self.jaConfig = json_file
        self.activeConfig = file_
        return

    def saveConfig(self) -> bool:
        """ Save a config into the class """
        file_ = eggUtils.abs_path(__file__) + '/config/joinActions.json'
        path = pathlib.Path('/'.join(file_.split('/')[:-1]))
        path.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_, 'w') as save_file:
                save_file.write(json.dumps(self.jaConfig, indent=4))
        except OSError:
            logger.error(f'File not be saved: {file_}', exc_info=True)
        return

    def getJoinMessage(self, guild: str, user: str) -> dict:
        """
        Returns any join messages to send

        Args:
            guild (str): ID of the guild
            user (str): ID of the user that joined

            Returns:
                (dict) :
                    {"status": True,
                     "response":
                        [{"message": "Message to send",
                         "channel": int},]
                    }
                    If status is fales, response contains reason why
                    If channel is blank, the message is intended to be a DM

            Raises:
                None
        """

        joinMessages = []
        results = self.readAll(guild)
        if not(results["status"]):
            logger.debug(f'Guild not configured: {guild}')
            return {"status": False, "response": "Guild not configured"}
        actions = results["response"]
        logger.debug(f'joinActions found: {actions}')

        for a in actions:
            if a["active"]:
                try:
                    joinMessages.append({"message": a["message"],
                                        "channel": int(a["channel"])})
                except ValueError as err:
                    logger.warning(f"Bad join action: {guild} | {a} | {err}")
                    continue
        if not(len(joinMessages)):
            logger.debug('No active join actions found')
            return {"status": False, "response": "No join actions found"}
        logger.debug(f'Join actions: {joinMessages}')
        return {"status": True, "response": joinMessages}

    async def onJoin(self, member, **kwargs) -> bool:
        """
        Hook method to be called from core script on Join event

        Return value controls if additional mod calls are performed. If True
        the core script should continue with calls. If False the core script
        should break from iterations.

        Args:
            member (discord.member) : a discord.member class
            **kwargs :

        Returns:
            (boolean)

        Raises:
            None
        """

        # These should be in a config - FUTURE MODULE replaceTags
        lsHolders = ['[MENTION]', '[USERNAME]', '[GUILDNAME]', '\\n']
        lsMember = [member.mention, member.display_name,
                    member.guild.name, '\n']

        jaResults = self.getJoinMessage(str(member.guild.id), str(member.id))
        if not(jaResults["status"]):
            return True

        for a in jaResults["response"]:
            if not(len(a["message"])):
                logger.warning('Blank message found, skipping')
                continue
            # START: Make replacements for tags - MOVE TO MODULE IN FUTURE
            for rp in lsHolders:
                a["message"] = a["message"].replace(rp, lsMember[lsHolders.index(rp)])  # noqa: E501
            # END
            if a["channel"]:
                logger.info(f'Sending Chat message to channel: {a["channel"]}')
                chatRoom = member.guild.get_channel(a["channel"])

                if not(chatRoom):
                    logger.warning(f'Channel not found: {a["channel"]}')
                else:
                    await chatRoom.send(a["message"])
            else:
                logger.info(f'Sending DM message to: {member.name}')
                await member.create_dm()
                await member.dm_channel.send(a["message"])
        return True

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
