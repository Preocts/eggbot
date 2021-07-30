"""
Process a member joining the server

Offers a simple configuration driven event handler for when a member
joins a Discord guild. With room to expand, this offer a great starter
module. Schedule a viewing before it is gone!

Author  : Preocts
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/eggbot
"""
from __future__ import annotations

import logging
from typing import Any
from typing import Dict
from typing import List
from typing import NamedTuple

from discord import Guild
from discord import Member
from discord.ext.commands import Cog

from eggbot.utils import tomlio


class JoinConfig(NamedTuple):
    """Configuration Model"""

    name: str
    channel: str
    message: str
    active: bool

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> JoinConfig:
        """Create a configuration model from dict"""
        return cls(
            name=str(config["name"]),
            channel=str(config["channel"]),
            message=str(config["message"]),
            active=bool(config["active"]),
        )


class MemberJoins(Cog):
    """Process members joining server"""

    EXTENSION_NAME: str = "JoinActions"
    EXTENSION_VERSION: str = "1.0.0"
    DEFAULT_CONFIG: str = "configs/memberjoins.toml"

    # Define by [TAG]: ["attr", "attr", ...]
    METADATA: Dict[str, List[str]] = {
        "[GUILDNAME]": ["guild", "name"],
        "[USERNAME]": ["name"],
        "[MENTION]": ["mention"],
    }

    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.logger.info("Loading MemberJoins...")
        super().__init__()
        self.config = tomlio.load(self.DEFAULT_CONFIG)

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        """OnJoin event hook for discord client"""
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

    def format_content(self, content: str, member: Member) -> str:
        """Replaced metadata tags in content, returns new string"""
        new_content = content
        for metatag, attribs in self.METADATA.items():
            replace: Any = ""
            for attr in attribs:
                replace = getattr(replace, attr) if replace else getattr(member, attr)
            new_content = new_content.replace(metatag, replace)
        return new_content

    def get_actions(self, guild_id: str) -> List[JoinConfig]:
        """Return a list of JoinConfig for a guild. Will be empty if not found"""
        config = self.config.get(guild_id)
        if config is None:
            return []
        return [JoinConfig.from_dict(action) for action in config]

    async def _send_channel(self, content: str, channel_id: str, guild: Guild) -> None:
        """Send a message to a specific channel within guild"""
        channel = guild.get_channel(int(channel_id))
        if channel is None:
            self.logger.warning("'%s' channel not found in %s", channel, guild.name)
        else:
            self.logger.info("Join message sent to '%s' in '%s'", channel, guild.name)
            await channel.send(content)

    async def _send_dm(self, content: str, member: Member) -> None:
        """Send a direct message to given member"""
        if not member.dm_channel:
            await member.create_dm()
        if not member.dm_channel:
            self.logger.info("DM to '%s' not allowed.", member.name)
        else:
            await member.dm_channel.send(content)
