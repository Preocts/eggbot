#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Something undefined

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
import os
from datetime import datetime
from typing import Any
from typing import Coroutine
from typing import Dict
from typing import List
from typing import MutableSet
from typing import NamedTuple
from typing import Optional

from discord import Guild
from discord import Message
from discord import TextChannel
from discord.errors import Forbidden
from discord.errors import HTTPException
from discord.errors import NotFound

from eggbot.configfile import ConfigFile

AUTO_LOAD: str = "Audit"


class AuditResults(NamedTuple):
    """Data class for audit results"""

    counter: int
    channel: str
    channel_id: int
    authors: MutableSet[str]
    start: datetime
    end: Optional[datetime] = None


# Protocols
msg_datetime = Coroutine[Any, Any, Optional[datetime]]
audit_results = Coroutine[Any, Any, Optional[AuditResults]]


class Audit:
    """Kudos points brought to Discord"""

    logger = logging.getLogger(__name__)
    MODULE_NAME: str = "Audit"
    MODULE_VERSION: str = "1.0.0"
    DEFAULT_CONFIG: str = "configs/audit.json"
    COMMAND_CONFIG: Dict[str, str] = {
        "audit!here": "audit_here",
        "audit!channel": "audit_channel",
        "audit!help": "print_help",
    }

    def __init__(self, config_file: str = DEFAULT_CONFIG) -> None:
        """Create instance and load configuration file"""
        self.logger.info("Initializing Audit module")
        self.owner = os.getenv("BOT_OWNER", "")
        self.config = ConfigFile()
        self.config.load(config_file)
        self.allow_list: List[str] = self.config.config.get("allow-list", [])
        if not self.config.config:
            self.config.create("module", self.MODULE_NAME)
            self.config.create("version", self.MODULE_VERSION)

    async def print_help(self, message: Message) -> None:
        """Prints help"""
        help_msg: List[str] = [
            "`audit!here [Start Message ID] (End Message ID)`\n",
            "Will audit all messages in current channel from start message",
            "to option end message. If end message ID not provided audit",
            "will include all messages since start message ID.\n\n",
            "`audit!channel [Channel ID] [Start Message ID] (End Message ID)`\n",
            "Will run the audit on the given channel ID and post result in",
            "current channel. Channel ID must be in the same guild.",
        ]

        await message.channel.send("".join(help_msg))

    async def audit_channel(self, message: Message) -> Optional[AuditResults]:
        """Run audit against given channel, return output or None"""
        channel_id = self.pull_msg_arg(message.content, 1)
        start_msg_id = self.pull_msg_arg(message.content, 2)
        end_msg_id = self.pull_msg_arg(message.content, 3)

        if channel_id is None or start_msg_id is None:
            return None

        channel = self._get_text_channel(message.guild, channel_id)

        if channel is None:
            return None

        return await self.run_audit(channel, start_msg_id, end_msg_id)

    async def audit_here(self, message: Message) -> Optional[AuditResults]:
        """Run audit in current channel, return output or None"""
        start_msg_id = self.pull_msg_arg(message.content, 1)
        end_msg_id = self.pull_msg_arg(message.content, 2)

        if start_msg_id is None:
            return None

        return await self.run_audit(message.channel, start_msg_id, end_msg_id)

    async def run_audit(
        self,
        channel: TextChannel,
        start_msg_id: int,
        end_msg_id: Optional[int],
    ) -> Optional[AuditResults]:
        """Runs audit on given channel, starting point and ending point"""
        start_time = await self._get_timestamp(channel, start_msg_id)
        audit: Optional[AuditResults] = None

        if start_time and not end_msg_id:
            audit = await self._get_auditresults(channel, start_time)
        elif start_time and end_msg_id:
            end_time = await self._get_timestamp(channel, end_msg_id)
            audit = await self._get_auditresults(channel, start_time, end_time)

        return audit

    def _get_text_channel(
        self,
        guild: Guild,
        channel_id: int,
    ) -> Optional[TextChannel]:
        """Fetches text channel, if exists, from guild"""
        return guild.get_channel(channel_id)

    async def _get_timestamp(
        self,
        channel: TextChannel,
        msg_id: int,
    ) -> Optional[datetime]:
        """Pull the datetime of a message ID, returns None if not found"""
        try:
            msg = await channel.fetch_message(msg_id)
        except (NotFound, Forbidden, HTTPException) as err:
            self.logger.error("Error fetching message: %s", err)
            msg = None

        return msg if msg is None else msg.created_at

    async def _get_auditresults(
        self,
        channel: TextChannel,
        start: datetime,
        end: Optional[datetime] = None,
    ) -> AuditResults:
        """Returns AuditResults from starttime to current, or end if provided"""
        counter: int = 0
        name_set: MutableSet[str] = set()
        if end is None:
            history_cor = channel.history(after=start)
        else:
            history_cor = channel.history(after=start, before=end)

        async for past_message in history_cor:
            counter += 1
            name_set.add(f"{past_message.author} ({past_message.author.id})")

        return AuditResults(
            counter=counter,
            channel=channel.name,
            channel_id=channel.id,
            authors=name_set,
            start=start,
            end=end,
        )

    async def on_message(self, message: Message) -> None:
        """ON MESSAGE event hook"""
        if str(message.channel.type) != "text":
            self.logger.debug("Not text channel")
            return

        if str(message.author.id) not in self.allow_list:
            self.logger.debug("Not the mama")
            return

        if not message.content.startswith("audit!"):
            self.logger.debug("Not the magic words")
            return

        audit_result: Optional[AuditResults] = None

        try:
            command = getattr(self, self.COMMAND_CONFIG[message.content.split()[0]])
            audit_result = await command(message)

        except (KeyError, AttributeError):
            pass

        if audit_result is not None:

            output_names = "\n".join(audit_result.authors)
            output_top = f"Audit: {audit_result.channel} ({audit_result.channel_id})\n"
            output_range = f"Start: {audit_result.start} - End: {audit_result.end}\n"
            output_desc = f"Of {audit_result.counter} messages the unique names are:\n"
            output_msg = f"{output_top}{output_range}{output_desc}```{output_names}```"

            await message.channel.send(output_msg)

    @staticmethod
    def pull_msg_arg(msg: str, pos: int = 1) -> Optional[int]:
        """Pulls the message ID aurgument, validate, and returns. None if invalid"""
        if len(msg.split()) >= 2:
            try:
                return int(msg.split()[pos])
            except (ValueError, IndexError):
                pass
        return None
