#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Respond to a member joining a guild

Offers a simple configuration driven event handler for when a member
joins a Discord guild. With room to expand, this offer a great starter
module. Schedule a viewing before it is gone!

TODO:
    - CLI controls

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from __future__ import annotations

import logging
from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple

from eggbot.configfile import ConfigFile

MODULE_NAME = "JoinActions"
MODULE_VERSION = "1.0.0"
DEFAULT_CONFIG = "configs/joinactions.json"


class JoinConfig(NamedTuple):
    """ Configuration Model """

    name: str
    channel: str
    message: str
    active: bool

    def __str__(self) -> str:
        """ Clean print of contents """
        return f"{self.name}, {self.channel}, {self.active}"

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> JoinConfig:
        """ Create a configuration model from dict """
        return cls(
            name=str(config["name"]),
            channel=str(config["channel"]),
            message=str(config["message"]),
            active=bool(config["active"]),
        )


class JoinActions:
    """ Respond to an 'on join' event from Discord """

    logger = logging.getLogger(__name__)

    def __init__(self, config_file: str = DEFAULT_CONFIG) -> None:
        """ Create instance and load configuration file """
        self.logger.info("Initializing JoinAction module")
        self.config = ConfigFile()
        self.config.load(config_file)
        if not self.config.config:
            self.config.create("module", MODULE_NAME)
            self.config.create("version", MODULE_VERSION)
        else:
            if self.config.read("module") != MODULE_NAME:
                self.logger.warning("JoinAction config module name mismatch!")
            if self.config.read("version") != MODULE_VERSION:
                self.logger.warning("JoinAction config version mismatch!")

    def get_actions(self, guild_id: str) -> List[JoinConfig]:
        """ Return a list of JoinConfig for a guild. Will be empty if not found """
        config = self.config.read(guild_id)
        if config:
            return [JoinConfig.from_dict(action) for action in config]
        return []
