#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from typing import Any
from typing import List
from typing import Dict
from typing import NamedTuple

from discord import Message  # type: ignore

from eggbot.configfile import ConfigFile

MODULE_NAME: str = "ChatKudos"
MODULE_VERSION: str = "1.0.0"
DEFAULT_CONFIG: str = "configs/chatkudos.json"
COMMAND_CONFIG: Dict[str, str] = {
    "kudos!max": "set_max",
    "kudos!gain": "set_gain",
    "kudos!loss": "set_loss",
}


class KudosConfig(NamedTuple):
    """ Config model for a guild in ChatKudos """

    roles: List[str] = []
    users: List[str] = []
    max: int = 5
    lock: bool = False
    gain_message: str = "[POINTS] to [NICKNAME]! That gives them [TOTAL] total!"
    loss_message: str = "[POINTS] from [NICKNAME]! That leaves them [TOTAL] total!"
    scores: Dict[str, int] = {}

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> KudosConfig:
        """ Create model from loaded config segment """
        return cls(
            roles=config.get("roles", []),
            users=config.get("users", []),
            max=config.get("max", 5),
            lock=config.get("lock", False),
            gain_message=config.get(
                "gain_message",
                "[POINTS] to [NICKNAME]! That gives them [TOTAL] total!",
            ),
            loss_message=config.get(
                "loss_message",
                "[POINTS] from [NICKNAME]! That gives them [TOTAL] total!",
            ),
            scores=config.get("scores", {}),
        )

    def as_dict(self) -> Dict[str, Any]:
        """ Returns NamedTuple as Dict """
        return self._asdict()  # pylint: disable=E1101


class ChatKudos:
    """ Kudos points brought to Discord """

    logger = logging.getLogger(__name__)

    def __init__(self, config_file: str = DEFAULT_CONFIG) -> None:
        """ Create instance and load configuration file """
        self.logger.info("Initializing ChatKudos module")
        self.config = ConfigFile()
        self.config.load(config_file)
        if not self.config.config:
            self.config.create("module", MODULE_NAME)
            self.config.create("version", MODULE_VERSION)
        else:
            if self.config.read("module") != MODULE_NAME:
                self.logger.warning("ChatKudos config module name mismatch!")
            if self.config.read("version") != MODULE_VERSION:
                self.logger.warning("ChatKudos config version mismatch!")

    def get_guild(self, guild_id: str) -> KudosConfig:
        """ Load a guild from the config, return defaults if empty """
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
        )
        if not self.config.read(guild_id):
            self.config.create(guild_id, new_conf.as_dict())
        else:
            self.config.update(guild_id, new_conf.as_dict())

    def set_max(self, message: Message) -> str:
        """ Set max number of points to be gained in one line """
        self.logger.debug("Set %s max: %s", message.guild.name, message.content)
        try:
            max_ = int(message.content.replace("kudos!max", ""))
        except ValueError:
            return "Usage: `kudo!max [N]` where N is a number."
        self.save_guild(str(message.guild.id), max=max_)
        if max_ > 0:
            return f"Max points set to {max_}"
        return "Max points set to unlimited"

    def set_gain(self, message: Message) -> str:
        """ Update the gain message of a guild """
        content = message.content.replace("kudos!gain", "").strip()
        return self._set_message(str(message.guild.id), {"gain_message": content})

    def set_loss(self, message: Message) -> str:
        """ Update the loss message of a guild """
        content = message.content.replace("kudos!loss", "").strip()
        return self._set_message(str(message.guild.id), {"loss_message": content})

    def _set_message(self, guild_id: str, content: Dict[str, str]) -> str:
        """ Sets and saves gain/loss messages """
        self.save_guild(guild_id, **content)
        return "Message has been set."

    def parse_command(self, message: Message) -> str:
        """ Process all commands prefixed with 'kudos!' """
        self.logger.debug("Parsing command: %s", message.content)
        command = message.content.split()[0]
        try:
            return getattr(self, COMMAND_CONFIG[command])(message)
        except (AttributeError, KeyError):
            self.logger.error("'%s' attribute not found!", command)
        return ""
