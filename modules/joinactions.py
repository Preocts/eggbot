#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Respond to a member joining a guild

Offers a simple configuration driven event handler for when a member
joins a Discord guild. With room to expand, this offer a great starter
module. Schedule a viewing before it is gone!

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

from discord import Member  # type: ignore
from discord import Guild  # type: ignore

from eggbot.configfile import ConfigFile

AUTO_LOAD: str = "JoinActions"
MODULE_NAME: str = "JoinActions"
MODULE_VERSION: str = "1.0.0"
DEFAULT_CONFIG: str = "configs/joinactions.json"

# Define by [TAG]: ["attr", "attr", ...]
METADATA: Dict[str, List[str]] = {
    "[GUILDNAME]": ["guild", "name"],
    "[USERNAME]": ["name"],
    "[MENTION]": ["mention"],
}


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

    @staticmethod
    def format_content(content: str, member: Member) -> str:
        """ Replaced metadata tags in content, returns new string """
        new_content = content
        for metatag, attribs in METADATA.items():
            replace: Any = ""
            for attr in attribs:
                replace = getattr(replace, attr) if replace else getattr(member, attr)
            new_content = new_content.replace(metatag, replace)
        return new_content

    def get_actions(self, guild_id: str) -> List[JoinConfig]:
        """ Return a list of JoinConfig for a guild. Will be empty if not found """
        config = self.config.read(guild_id)
        if not config:
            return []
        return [JoinConfig.from_dict(action) for action in config]

    async def onjoin(self, member: Member) -> None:
        """ OnJoin event hook for discord client """
        self.logger.info("On Join event: %s, %s", member.guild.name, member.name)

        if member.bot:
            return None

        actions = self.get_actions(str(member.guild.id))

        if not actions:
            self.logger.debug("No actions defined for '%s'", member.guild.id)
            return None

        for action in actions:
            if not action.active:
                continue
            content = self.format_content(action.message, member)
            if action.channel:
                await self._send_channel(content, action.channel, member.guild)
            else:
                await self._send_dm(content, member)

    async def _send_channel(self, content: str, channel_id: str, guild: Guild) -> None:
        """ Send a message to a specific channel within guild """
        channel = guild.get_channel(int(channel_id))
        if not channel:
            self.logger.warning("'%s' channel not found in %s", channel, guild.name)
        else:
            await channel.send(content)

    async def _send_dm(self, content: str, member: Member) -> None:
        """ Send a direct message to given member """
        if not member.dm_channel:
            await member.create_dm()
        if not member.dm_channel:
            self.logger.info("DM to '%s' not allowed.", member.name)
        else:
            await member.dm_channel.send(content)
