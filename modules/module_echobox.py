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
from typing import NamedTuple

from discord import Message  # type: ignore
from discord import TextChannel  # type: ignore
from discord import User  # type: ignore

from eggbot.discordclient import DiscordClient

AUTO_LOAD: str = "EchoBox"


class ReturnMessage(NamedTuple):
    """ Data model for return values of parse command """

    channel: str = ""
    owner: str = ""


class EchoBox:
    """ Talk to a chennel through the bot """

    MODULE_NAME: str = "EchoBox"
    MODULE_VERSION: str = "1.0.0"
    COMMAND_CONFIG: Dict[str, str] = {
        "echo!set": "set_connection",
        "echo!start": "start_echo",
        "echo!stop": "stop_echo",
    }
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        """ Create instance and load configuration file """
        self.logger.info("Initializing EchoBox module")

        self.discord = DiscordClient()
        self.owner_id: str = os.getenv("BOT_OWNER", "")
        self.owner: Optional[User] = None

        # TODO: Implement these
        self.target_channel: Optional[TextChannel] = None
        self.target_use_mark: float = 0.0

        if not self.owner_id:
            self.logger.warning("BOT_OWNER not set in '.env'. EchoBox disabled.")

    def __populate_owner(self) -> None:
        """ Looks up owner by ID, returns None if not found """
        if self.owner is not None or not self.owner_id:
            return

        try:
            self.owner = self.discord.client.get_user(int(self.owner_id))
        except ValueError:
            self.owner_id = ""

    async def __send_to_user(self, user: User, author: str, content: str) -> None:
        """ Sends a DM to the provided discord.User """
        self.logger.debug("Prepping DM to '%s'", user.name)
        if user.dm_channel:
            await user.create_dm()

        if not user.dm_channel:
            self.logger.error("Cannot open DM for %s. Deactivating EchoBox.", user.name)
            self.owner_id = ""
            self.owner = None
        else:
            await user.send(f"EchoBox: DM to bot from {author}\n```{content}```")
            self.logger.info("DM send.")

    def parse_command(self, message: Message) -> ReturnMessage:
        """ Runs commands, returns messages to send """
        command = message.content.split()[0]
        responses = ReturnMessage()
        try:
            responses = getattr(self, self.COMMAND_CONFIG[command])(message)
        except KeyError:
            self.logger.info("Unknown command passed: %s", command)
        except AttributeError:
            self.logger.error("Attribute not defined for command: %s", command)
        return responses

    async def on_message(self, message: Message) -> None:
        """ ON MESSAGE event hook """
        if str(message.channel.type) != "private" or not self.owner_id:
            return
        self.logger.debug("Got message: %s", message)
        self.__populate_owner()

        if message.content.startswith("echo!"):
            result = self.parse_command(message)
            self.logger.info("Results: %s", result)
        elif self.owner is not None:
            await self.__send_to_user(self.owner, message.author.name, message.content)
