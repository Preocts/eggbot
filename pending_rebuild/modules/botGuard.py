# -*- coding: utf-8 -*-
""" botGuard only allows specific bots to join a guild

    Created by Preocts
        Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot

    When a bot joins the guild this module will check an allow list for
    the bot's ID. If not found the bot will be immediately kicked provided
    the bot running this module has permissions to do so.

    A message will be posted to a selected channel telling members of the
    action, providing the bot's ID, and mentioning how to allow list
    a bot with that ID.

    Checklist:

    - [x] Load config or create new
    - [x] Save config and create new file/path
    - [x] Check if config has guild (build defaults if needed)
    - [x] Active toggle
    - [x] Control commands
      - [x] Guild owner access only
      - [x] guard!help : Display help
      - [x] guard!on : Turn gaurd on
      - [x] guard!off : Turn guard off
      - [x] guard!allow [member id] : Add/Remove provided ID
      - [x] guard!channel [#channel] : Set sqwuak channel
      - [x] guard!fail [messge] : Set denied entry message
      - [x] guard!pass [message] : Set allowed entry message
    - [x] onJoin action
      - [x] Check if joining member is a bot (discord.member.bot)
      - If bot:
        - [x] Kick if discord.member.id not on allow list
        - [x] Announce action in announce_channel of config
        - [x] If channel is not set, DM guild owner
"""

import json
import logging
import pathlib
from eggbot.utils import eggUtils

logger = logging.getLogger(__name__)  # Create module level logger


def initClass():
    """ A fucntion to allow automated creation of a class instance """
    return botGuard()


def debug_logger(func):
    """ Small wrapper to log entry and exit values """

    def wrapper(*args, **kwargs):
        logger.debug(f"[START] {func.__name__} : {args[1:]}, {kwargs}")
        return_value = func(*args, **kwargs)
        logger.debug(f"[FINISH] {func.__name__} : {return_value}")
        return return_value

    return wrapper


class botGuard:
    """
    Defines the BotGuard Object

    Config format:
    {
        "discord.guild.id" {
            "owner": "discord.member.id"
            "active": true,
            "allowed": [ "discord.member.id" ],
            "channel": "discord.channel.id",
            "content_deny": "Message when a bot is kicked",
            "content_allow": "Message when a bot is allowed"
        }
    }
    """

    name = "botGuard"
    version = "v1.0"
    allowReload = True
    instCount = 0

    def __init__(self) -> None:
        """INIT"""
        logging.info("Start: Initializing botGuard")
        self.bgConfig = {}
        self.activeConfig = ""
        self.loadConfig()
        botGuard.instCount += 1
        logger.info(f"Config loaded with {len(self.bgConfig)} guild entries")
        return

    def __str__(self) -> None:
        return str(self.bgConfig)

    def __bool__(self) -> None:
        if len(self.bgConfig):
            return True
        return False

    __nonzero__ = __bool__

    def __del__(self) -> None:
        """ Save configs on exit """
        self.saveConfig()
        botGuard.instCount -= 1
        return

    @debug_logger
    def loadConfig(self) -> None:
        """ Load a config into the class """
        file_ = eggUtils.abs_path(__file__) + "/config/botGuard.json"
        json_file = {}
        try:
            with open(file_, "r") as load_file:
                json_file = json.load(load_file)
        except json.decoder.JSONDecodeError:
            logger.error("Config file empty or bad format. ", exc_info=True)
        except FileNotFoundError:
            logger.error(f"Config file not found: {file_}", exc_info=True)

        self.bgConfig = json_file
        self.activeConfig = file_
        return

    @debug_logger
    def saveConfig(self) -> bool:
        """ Save a config into the class """
        file_ = eggUtils.abs_path(__file__) + "/config/botGuard.json"
        path = pathlib.Path("/".join(file_.split("/")[:-1]))
        path.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_, "w") as save_file:
                save_file.write(json.dumps(self.bgConfig, indent=4))
        except OSError:
            logger.error(f"File not be saved: {file_}", exc_info=True)
        return

    @debug_logger
    def config_check(self, guild) -> None:
        """Ensures the config is healthy, builds guild if needed

        Args:
            [discord.guild] : Discord Guild class
        """
        guild_id = str(guild.id)
        owner_id = str(guild.owner_id)
        if not (isinstance(self.bgConfig, dict)):
            logger.warning("Config file was not a json. Fixing")
            self.bgConfig = {}

        if self.bgConfig.get(guild_id) is None:
            logger.info(
                "Adding guild to config with defaults "
                f"{guild_id}, {guild.name}"
            )
            self.bgConfig[guild_id] = {
                "owner": owner_id,
                "active": False,
                "allowed": [],
                "channel": "",
                "content_deny": "A bot with id ({id}) joined and I was not "
                "told! I have kicked it out. Now clap :clap:",
                "content_allow": "The bot with id ({id}) you told me about is "
                "here now. Just an FYI.",
            }
            self.saveConfig()
        return

    @debug_logger
    def active_toggle(self, guild, state: bool) -> str:
        """Toggles the active flag for a guild

        Args:
            [discord.guild] : Discord Guild class
            [bool] : What state the flag is to be set
        """
        response = "Bot Guard is now **inactive** for this guild."
        self.bgConfig[str(guild.id)]["active"] = state
        if self.bgConfig[str(guild.id)]["active"]:
            response = "Bot Guard is now **active** for this guild."
        return response

    @debug_logger
    def update_allowed(self, message) -> str:
        """Adds or removes a bot ID to the list of allowed bots for a guild

        Args:
            [discord.message] : Incoming message containing command
        """
        # guard!list [channelID]
        gid = str(message.guild.id)
        channel_id = message.clean_content.split(" ")
        channel_id = channel_id[1] if len(channel_id) > 1 else ""
        try:
            int(channel_id)
        except ValueError:
            err = "Incorrect command format, Member ID invalid"
            return err
        if channel_id in self.bgConfig[gid]["allowed"]:
            # Exists, remove by index
            idx = self.bgConfig[gid]["allowed"].index(channel_id)
            self.bgConfig[gid]["allowed"].pop(idx)
            response = f"Bot account removed from allow list: {channel_id}"
        else:
            # Append to list
            self.bgConfig[gid]["allowed"].append(channel_id)
            response = f"Bot account added to allow list: {channel_id}"
        return response

    @debug_logger
    def set_channel(self, message) -> str:
        """Sets the channel used to send alerts when another bot joins

        Args:
            [discord.message] : Incoming message containing command
        """
        # guard!channel [#channel]
        gid = str(message.guild.id)
        response = "Channel not found, be sure to #Channel when setting."
        if len(message.clean_content.split()) == 1:
            response = (
                "Channel removed. Guild owner will recieve DMs on "
                "any actions taken"
            )
            self.bgConfig[gid]["channel"] = ""
        for channel in message.channel_mentions:
            self.bgConfig[gid]["channel"] = str(channel.id)
            response = f"Channel set to {channel.name}"
            break
        return response

    @debug_logger
    def set_content(self, message, on_action: str) -> str:
        """Sets the message displayed when a bot is allowed or denied

        Args:
            [discord.message] : Incoming message containing command
            [str] : Action this message for.
                Can be 'content_deny' or 'content_allow'
        """
        gid = str(message.guild.id)
        content = " ".join(message.content.split(" ")[1:])
        self.bgConfig[gid][on_action] = content
        return f"Message now set to: {content}"

    @debug_logger
    def help_content(self) -> str:
        """ Returns a formatted string for chat display of guard!help """
        help_lines = [
            f"Bot Guard {botGuard.version} help:",
            "```",
            "guard!on",
            "\tTurn Bot Guard on.",
            "guard!off",
            "\tTurn Bot Guard off.",
            "guard!allow [memberID]",
            "\tAdds a bot ID to the allow-list which will stop Bot Guard from "
            "kicking that bot on join. If already listed the ID will be "
            "removed.",
            "guard!channel [#channel-mention]",
            "\tIf you want Bot Guard to announce any actions taken set a "
            "channel with this command. By default, guild owner is DM'ed "
            "on all actions.",
            "guard!fail [message]",
            "\tSet a custom message for when a bot is kicked automatically.",
            "guard!pass [message]",
            "\tSet a custom message for when a bot is allowed to join.",
            "guard!help",
            "\tDisplay this message." "```",
            "Documentation found here: https://github.com/Preocts/Egg_Bot/"
            "blob/source/docs/botGuard.md",
        ]
        return "\n".join(help_lines)

    @debug_logger
    def checkList(self, guild: str, bot: str) -> dict:
        """Checks the provided bot ID against allow list

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
            dict : {"status": (bool), "channel": (str), "response": (str)}

        Raises:
            None
        """
        # Is the guild active?
        if not (self.bgConfig[guild]["active"]):
            logger.info("Bot joined an inactive guild")
            return {
                "status": True,
                "channel": self.bgConfig[guild]["channel"],
                "response": "",
            }
        # Is the bot allowed?
        if bot in self.bgConfig[guild]["allowed"]:
            # Yup. *notices your backstage pass* OwO what's this?
            logger.info("Bot was allowed to join")
            return {
                "status": True,
                "channel": self.bgConfig[guild]["channel"],
                "response": self.bgConfig[guild]["content_allow"],
            }
        # Nope. OwO I won't miss binch *pulls trigger*
        logger.warning("Bot joined that was not allowed.")
        return {
            "status": False,
            "channel": self.bgConfig[guild]["channel"],
            "response": self.bgConfig[guild]["content_deny"],
        }

    @debug_logger
    async def onJoin(self, **kwargs) -> None:
        """Hook method to be called from core script on Join event

        Keyword Args:
            member (discord.member): a discord.member class
        """
        member = kwargs.get("member")
        self.config_check(member.guild)
        # Is this join a bot?
        if not (member.bot):
            return
        # Handle it *gun cocks*
        logger.info("Bot join detected...")
        bgResults = self.checkList(str(member.guild.id), str(member.id))
        if not (bgResults["status"]):
            # This bot is not allowed
            await member.kick(reason="This bot was not approved to join.")
        if not bgResults["response"]:
            return
        if not (bgResults["channel"]):
            # DM Owner
            response = bgResults["response"].replace("{id}", str(member.id))
            await member.guild.owner.create_dm()
            await member.guild.owner.dm_channel.send(response)
            return
        ch = member.guild.get_channel(int(bgResults["channel"]))
        await ch.send(bgResults["response"].replace("{id}", str(member.id)))
        return

    @debug_logger
    async def onMessage(self, **kwargs) -> None:
        """Hook method to be called from core script on Message event

        Keyword Args:
            message (discord.message) : a discord.message class
        """
        Supported_Channels = "<class 'discord.channel.TextChannel'>"
        message = kwargs.get("message")
        guild_id = str(message.guild.id)
        if message is None:
            return
        if str(type(message.channel)) not in Supported_Channels:
            return
        self.config_check(message.guild)
        if str(message.author.id) not in self.bgConfig[guild_id]["owner"]:
            return
        Command_Set = {
            "guard!help": (self.help_content,),
            "guard!on": (self.active_toggle, message.guild, True),
            "guard!off": (self.active_toggle, message.guild, False),
            "guard!allow": (self.update_allowed, message),
            "guard!channel": (self.set_channel, message),
            "guard!fail": (self.set_content, message, "content_deny"),
            "guard!pass": (self.set_content, message, "content_allow"),
        }
        command = Command_Set.get(message.clean_content.split()[0], None)
        if command is None:
            return
        response = command[0](*command[1:])
        self.saveConfig()
        if response:
            await message.channel.send(response)
        return


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
