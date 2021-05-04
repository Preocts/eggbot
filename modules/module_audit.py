#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Something undefined

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
import logging
from typing import Dict
from typing import List
from typing import Optional
from typing import MutableSet

from discord import Message  # type: ignore

from eggbot.configfile import ConfigFile

AUTO_LOAD: str = "Audit"


class Audit:
    """ Kudos points brought to Discord """

    # pylint: disable=too-many-locals

    logger = logging.getLogger(__name__)
    MODULE_NAME: str = "Audit"
    MODULE_VERSION: str = "1.0.0"
    DEFAULT_CONFIG: str = "configs/audit.json"
    COMMAND_CONFIG: Dict[str, str] = {
        "audit!list": "audi_max",
    }

    def __init__(self, config_file: str = DEFAULT_CONFIG) -> None:
        """ Create instance and load configuration file """
        self.logger.info("Initializing Audit module")
        self.owner = os.getenv("BOT_OWNER", "")
        self.config = ConfigFile()
        self.config.load(config_file)
        self.allow_list: List[str] = self.config.config.get("allow-list", [])
        if not self.config.config:
            self.config.create("module", self.MODULE_NAME)
            self.config.create("version", self.MODULE_VERSION)

    async def on_message(self, message: Message) -> None:
        """ ON MESSAGE event hook """
        if str(message.channel.type) != "text":
            self.logger.debug("Not text channel")
            return

        if str(message.author.id) not in self.allow_list:
            self.logger.debug("Not the mama")
            return

        if not message.content.startswith("audit!list"):
            self.logger.debug("Not the magic words")
            return

        anchor_id = self.pull_anchor(message.content)
        stop_id = self.pull_anchor(message.content, 2)

        if anchor_id is None:
            self.logger.debug("Invalid anchor id")
            return

        # TODO: Refactor and wrap in Try NotFound, Forbidden, HTTPException
        anchor_msg: Message = await message.channel.fetch_message(anchor_id)
        if stop_id:
            stop_msg: Optional[Message] = await message.channel.fetch_message(stop_id)
        else:
            stop_msg = None

        anchor_dt = anchor_msg.created_at
        stop_dt = stop_msg.created_at if stop_msg else None

        counter: int = 0
        name_set: MutableSet[str] = set()
        if stop_dt is not None:
            history_cor = message.channel.history(after=anchor_dt, before=stop_dt)
        else:
            history_cor = message.channel.history(after=anchor_dt)

        async for past_message in history_cor:
            counter += 1
            name_set.add(f"{past_message.author} ({past_message.author.id})")

        output_names = "\n".join(name_set)
        output_header = f"Start: {anchor_dt} - End: {stop_dt}\n"
        output_desc = f"Of {counter} messages the unique names are:\n"
        output_msg = f"{output_header}{output_desc}```{output_names}```"

        await message.channel.send(output_msg)

    @staticmethod
    def pull_anchor(msg: str, pos: int = 1) -> Optional[int]:
        """ Pulls the message ID aurgument, validate, and returns. None if invalid """
        if len(msg.split()) >= 2:
            try:
                return int(msg.split()[pos])
            except (ValueError, IndexError):
                pass
        return None
