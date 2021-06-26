#!/usr/bin/env python3
"""
Kudos points brought to Discord

Chat Kudos are points that can be granted, or taken, from server
members by simply mentioning their name and having "+"s or "-"s
following the mention.  The bot will reply with a customizable
message, tell you how many kudos were just received, and keep a
running tally.

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from __future__ import annotations

import logging
import re
import time
from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional

from discord import Message

from eggbot.configfile import ConfigFile

AUTO_LOAD: str = "ChatKudos"
MODULE_NAME: str = "ChatKudos"
MODULE_VERSION: str = "1.0.0"
DEFAULT_CONFIG: str = "configs/chatkudos.json"
COMMAND_CONFIG: Dict[str, str] = {
    "kudos!max": "set_max",
    "kudos!gain": "set_gain",
    "kudos!loss": "set_loss",
    "kudos!user": "set_lists",
    "kudos!role": "set_lists",
    "kudos!lock": "set_lock",
    "kudos!help": "show_help",
    "kudos!board": "generate_board",
}


class KudosConfig(NamedTuple):
    """Config model for a guild in ChatKudos"""

    roles: List[str] = []
    users: List[str] = []
    max: int = 5
    lock: bool = False
    gain_message: str = "[POINTS] to [NICKNAME]! That gives them [TOTAL] total!"
    loss_message: str = "[POINTS] from [NICKNAME]! That leaves them [TOTAL] total!"
    scores: Dict[str, int] = {}

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> KudosConfig:
        """Create model from loaded config segment"""
        return cls(**config)

    def as_dict(self) -> Dict[str, Any]:
        """Returns NamedTuple as Dict"""
        return self._asdict()  # pylint: disable=E1101


class Kudos(NamedTuple):
    """Model for a Kudos"""

    user_id: str
    display_name: str
    amount: int
    current: int


class ChatKudos:
    """Kudos points brought to Discord"""

    logger = logging.getLogger(__name__)

    def __init__(self, config_file: str = DEFAULT_CONFIG) -> None:
        """Create instance and load configuration file"""
        self.logger.info("Initializing ChatKudos module")
        self.config = ConfigFile()
        self.config.load(config_file)
        if not self.config.config:
            self.config.create("module", MODULE_NAME)
            self.config.create("version", MODULE_VERSION)

    def get_guild(self, guild_id: str) -> KudosConfig:
        """Load a guild from the config, return defaults if empty"""
        self.logger.debug("Get guild '%s'", guild_id)
        guild_conf = self.config.read(guild_id)
        if not guild_conf:
            return KudosConfig()
        return KudosConfig.from_dict(guild_conf)

    def save_guild(self, guild_id: str, **kwargs: Any) -> None:
        """
        Save a guild entry. Any keyword excluded will save existing value.

        Keyword Args:
            roles: List[str], roles that can use when locked
            users: List[str], users that can use when locked
            max: int, max points granted in one line
            lock: bool, restict to `roles`/`users` or open to all
            gain_message: str, message displayed on gain of points
            loss_message: str, message displayed on loss of points
            scores: Dict[str, int], Discord user id paired with total Kudos
        """
        self.logger.debug("Save: %s, (%s)", guild_id, kwargs)
        guild_conf = self.get_guild(guild_id)
        new_conf = KudosConfig(
            roles=kwargs.get("roles", guild_conf.roles),
            users=kwargs.get("users", guild_conf.users),
            max=kwargs.get("max", guild_conf.max),
            lock=kwargs.get("lock", guild_conf.lock),
            gain_message=kwargs.get("gain_message", guild_conf.gain_message),
            loss_message=kwargs.get("loss_message", guild_conf.loss_message),
            scores=kwargs.get("scores", guild_conf.scores),
        )
        if not self.config.read(guild_id):
            self.config.create(guild_id, new_conf.as_dict())
        else:
            self.config.update(guild_id, new_conf.as_dict())

    def set_max(self, message: Message) -> str:
        """Set max number of points to be gained in one line"""
        self.logger.debug("Set %s max: %s", message.guild.name, message.content)
        try:
            max_ = int(message.content.replace("kudos!max", ""))
        except ValueError:
            return "Usage: `kudo!max [N]` where N is a number."
        self.save_guild(str(message.guild.id), max=max_)
        return f"Max points now: {max_}" if max_ > 0 else "Max points now: unlimited"

    def set_gain(self, message: Message) -> str:
        """Update the gain message of a guild"""
        content = message.content.replace("kudos!gain", "").strip()
        return self._set_message(str(message.guild.id), "gain_message", content)

    def set_loss(self, message: Message) -> str:
        """Update the loss message of a guild"""
        content = message.content.replace("kudos!loss", "").strip()
        return self._set_message(str(message.guild.id), "loss_message", content)

    def _set_message(self, guild_id: str, key: str, content: Dict[str, str]) -> str:
        """Sets and saves gain/loss messages"""
        if content:
            self.save_guild(guild_id, **{key: content})
            return "Message has been set."
        return ""

    def set_lists(self, message: Message) -> str:
        """Update user and role lists based on message mentions"""
        changes: List[str] = self._set_users_list(message)
        changes.extend(self._set_roles_list(message))

        return "Allow list changes: " + ", ".join(changes) if changes else ""

    def _set_users_list(self, message: Message) -> List[str]:
        """Process and user mentions in message, return changes"""
        changes: List[str] = []
        users = set(self.get_guild(str(message.guild.id)).users)

        for mention in message.mentions:
            if str(mention.id) in users:
                users.remove(str(mention.id))
                changes.append(f"**-**{mention.display_name}")
            else:
                users.add(str(mention.id))
                changes.append(f"**+**{mention.display_name}")
        if changes:
            self.logger.error(changes)
            self.save_guild(str(message.guild.id), users=list(users))
        return changes

    def _set_roles_list(self, message: Message) -> List[str]:
        """Process all role mentions in message, return changes"""
        changes: List[str] = []
        roles = set(self.get_guild(str(message.guild.id)).roles)

        for role_mention in message.role_mentions:
            if str(role_mention.id) in roles:
                roles.remove(str(role_mention.id))
                changes.append(f"**-**{role_mention.name}")
            else:
                roles.add(str(role_mention.id))
                changes.append(f"**+**{role_mention.name}")
        if changes:
            self.save_guild(str(message.guild.id), roles=list(roles))
        return changes

    def set_lock(self, message: Message) -> str:
        """Toggle lock for guild"""
        new_lock = not self.get_guild(str(message.guild.id)).lock
        self.save_guild(str(message.guild.id), lock=new_lock)
        if new_lock:
            return "ChatKudos is now locked. Only allowed users/roles can use it!"
        return "ChatKudos is now unlocked. **Everyone** can use it!"

    def show_help(self, message: Message) -> str:
        """Help and self-plug, yay!"""
        self.logger.debug("Help: %s", message.author.name)
        return (
            "Detailed use instructions here: "
            "https://github.com/Preocts/eggbot/blob/main/docs/chatkudos.md"
        )

    def generate_board(self, message: Message) -> str:
        """Create scoreboard"""
        self.logger.debug("Scoreboard: %s", message.content)
        try:
            count = int(message.content.replace("kudos!board", ""))
        except ValueError:
            count = 10
        guild_conf = self.get_guild(str(message.guild.id))
        # Make a list of keys (user IDs) sorted by their value (score) low to high
        id_list = sorted(guild_conf.scores, key=lambda key: guild_conf.scores[key])
        score_list: List[str] = [f"Top {count} ChatKudos holders:", "```"]
        while count > 0 and id_list:
            user_id = id_list.pop()
            user = message.guild.get_member(int(user_id))
            display_name = user.display_name if user else user_id
            score_list.append(
                "{:>5} | {:<38}".format(guild_conf.scores[user_id], display_name)
            )
            count -= 1
        score_list.append("```")
        return "\n".join(score_list)

    def find_kudos(self, message: Message) -> List[Kudos]:
        """Process a chat-line for Kudos"""
        kudos_list: List[Kudos] = []

        for mention in message.mentions:
            kudos = self._calc_kudos(message, str(mention.id))
            if kudos is None:
                continue
            current = self.get_guild(str(message.guild.id)).scores.get(
                str(mention.id), 0
            )
            kudos_list.append(
                Kudos(str(mention.id), mention.display_name, kudos, current)
            )
            self.logger.debug("Find Kudos: %s", kudos_list[-1])
        return kudos_list

    def _calc_kudos(self, message: Message, mention_id: str) -> Optional[int]:
        """Calculate the number of kudos given to a mention"""
        max_ = self.get_guild(str(message.guild.id)).max

        for idx, word in enumerate(message.content.split()):
            if not re.search(f"{mention_id}", word):
                continue
            try:
                next_word = message.content.split()[idx + 1]
            except IndexError:
                continue
            if "+" not in next_word and "-" not in next_word:
                continue

            point_change = next_word.count("+") - next_word.count("-")
            if max_ > 0 < point_change > max_:
                point_change = max_
            elif max_ > 0 > point_change < (max_ * -1):
                point_change = max_ * -1

            return point_change
        return None

    def apply_kudos(self, guild_id: str, kudos_list: List[Kudos]) -> None:
        """Update scores in config"""
        scores = self.get_guild(guild_id).scores
        for kudos in kudos_list:
            scores[kudos.user_id] = scores.get(kudos.user_id, 0) + kudos.amount

        self.save_guild(guild_id, scores=scores)

    def parse_command(self, message: Message) -> str:
        """Process all commands prefixed with 'kudos!'"""
        self.logger.debug("Parsing command: %s", message.content)
        command = message.content.split()[0]
        try:
            result = getattr(self, COMMAND_CONFIG[command])(message)
        except (AttributeError, KeyError):
            self.logger.error("'%s' attribute not found!", command)
            return ""
        return result

    def is_command_allowed(self, message: Message) -> bool:
        """Determine if author of message can run commands"""
        if str(message.author.id) == str(message.guild.owner.id):
            return True

        if str(message.author.id) in self.get_guild(str(message.guild.id)).users:
            return True

        return False

    def is_kudos_allowed(self, message: Message) -> bool:
        """Determine if author can grant kudos"""
        allowed_roles = self.get_guild(str(message.guild.id)).roles

        if not self.get_guild(str(message.guild.id)).lock:
            return True

        for role in message.author.roles:
            if str(role.id) in allowed_roles:
                return True

        return self.is_command_allowed(message)

    async def on_message(self, message: Message) -> None:
        """On Message event hook for bot"""
        if not message.content or str(message.channel.type) != "text":
            return

        tic = time.perf_counter()
        self.logger.debug("[START] onmessage - ChatKudos")

        if message.content.startswith("kudos!") and self.is_command_allowed(message):
            response = self.parse_command(message)
            if response:
                await message.channel.send(response)
                self.config.save()
            return

        if not (message.mentions and self.is_kudos_allowed(message)):
            return

        kudos_list = self.find_kudos(message)
        self.apply_kudos(str(message.guild.id), kudos_list)
        await self._announce_kudos(message, kudos_list)
        self.config.save()

        toc = time.perf_counter()
        self.logger.debug("[FINISH] onmessage: %f ms", round(toc - tic, 2))

    async def _announce_kudos(self, message: Message, kudos_list: List[Kudos]) -> None:
        """Send any Kudos to the chat"""
        for kudos in kudos_list:
            if kudos.amount < 0:
                msg = self.get_guild(str(message.guild.id)).loss_message
            else:
                msg = self.get_guild(str(message.guild.id)).gain_message

            await message.channel.send(self._format_message(msg, kudos))

    @staticmethod
    def _format_message(content: str, kudos: Kudos) -> str:
        """Apply metadata replacements"""
        new_total = kudos.current + kudos.amount

        formatted_msg = content.replace("[POINTS]", str(kudos.amount))
        formatted_msg = formatted_msg.replace("[NAME]", kudos.display_name)
        formatted_msg = formatted_msg.replace("[TOTAL]", str(new_total))

        return formatted_msg
