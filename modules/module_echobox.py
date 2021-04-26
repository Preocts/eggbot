#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Echo box, makes the bot echo a DM to a given guild and channel

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
import logging
from typing import Dict
from typing import Optional

from discord import Message  # type: ignore
from discord import TextChannel  # type: ignore
from discord import User  # type: ignore

from eggbot.discordclient import DiscordClient

AUTO_LOAD: str = "EchoBox"
MODULE_NAME: str = "EchoBox"
MODULE_VERSION: str = "1.0.0"
COMMAND_CONFIG: Dict[str, str] = {
    "echo!set": "set_connection",
    "echo!start": "start_echo",
    "echo!stop": "stop_echo",
}


class EchoBox:
    """ Talk to a chennel through the bot """

    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        """ Create instance and load configuration file """
        self.logger.info("Initializing EchoBox module")
        self.discord = DiscordClient()
        self.target_channel: Optional[TextChannel] = None
        self.owner: Optional[User] = None
        self.disabled: bool = False

    def __get_user(self, member_id: str) -> Optional[User]:
        """ Looks up a user by ID, returns None if not found """
        try:
            print(f"rooJade Looking for {member_id}")
            return self.discord.client.get_user(int(member_id))
        except ValueError:
            print("rooD NOT A NUMBER")
            return None

    async def __send_to_owner(self, content: str) -> None:
        """ Sends a DM to the registered bot owner """
        if not self.owner:
            self.logger.warning("BOT_OWNER not set in '.env'. EchoBox disabled.")
            self.disabled = True
            return

        if not self.owner.dm_channel:
            await self.owner.create_dm()

        if not self.owner.dm_channel:
            self.logger.error("Unable to open DM to owner. Deactivating EchoBox.")
            self.owner = None
        else:
            await self.owner.send(f"EchoBox: DM to bot\n```{content}```")

    async def on_message(self, message: Message) -> None:
        """ ON MESSAGE event hook """
        if str(message.channel.type) != "private" and not self.disabled:
            return
        self.logger.debug("Got message: %s", message)

        if message.content.startswith("echo!"):
            # TODO handle command
            pass
        else:
            self.owner = self.__get_user(os.getenv("BOT_OWNER", ""))
            await self.__send_to_owner(message.content)
