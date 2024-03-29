#!/usr/bin/env python3
"""
Echo box, makes the bot echo a DM to a given guild and channel

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
import os
import time
from typing import Dict
from typing import NamedTuple
from typing import Optional

from discord import Client
from discord import Message
from discord import TextChannel
from discord import User

AUTO_LOAD: str = "EchoBox"


class ReturnMessage(NamedTuple):
    """Data model for return values of parse command"""

    channel: str = ""
    owner: str = ""


class EchoBox:
    """Talk to a chennel through the bot"""

    MODULE_NAME: str = "EchoBox"
    MODULE_VERSION: str = "1.0.0"
    COMMAND_CONFIG: Dict[str, str] = {
        "echo!set": "set_connection",
        "echo!send": "send_echo",
        "echo!stop": "stop_echo",
    }
    logger = logging.getLogger(__name__)

    def __init__(self, client: Client) -> None:
        """Create instance and load configuration file"""
        self.logger.info("Initializing EchoBox module")

        self.client = client
        self.owner_id: str = os.getenv("BOT_OWNER", "")
        self.owner: Optional[User] = None

        self.target_channel: Optional[TextChannel] = None
        self.target_use_mark: float = 0.0
        self.expirey: int = 180

        if not self.owner_id:
            self.logger.warning("BOT_OWNER not set in '.env'. EchoBox disabled.")

    def __populate_owner(self) -> None:
        """Looks up owner by ID, returns None if not found"""
        if self.owner is not None or not self.owner_id:
            return

        try:
            self.owner = self.client.client.get_user(int(self.owner_id))
        except ValueError:
            self.owner_id = ""

    async def __send_to_owner(self, content: str) -> None:
        """Sends a DM to the provided discord.User"""
        if not self.owner or not content:
            return

        self.logger.debug("Prepping DM to '%s'", self.owner.name)

        if self.owner.dm_channel:
            await self.owner.create_dm()

        if not self.owner.dm_channel:
            self.logger.error("Cannot DM '%s'. Deactivating EchoBox.", self.owner.name)
            self.owner_id = ""
            self.owner = None
        else:
            await self.owner.send(content)
            self.logger.info("DM sent.")

    async def __send_to_channel(self, content: str) -> None:
        """Send a message to the provided channel"""
        if not self.target_channel or not content:
            return

        self.logger.debug("Prepping channel message to '%s'", self.target_channel.name)

        await self.target_channel.send(content)

    def parse_command(self, message: Message) -> ReturnMessage:
        """Runs commands, returns messages to send"""
        command = message.content.split()[0]
        responses = ReturnMessage()
        try:
            responses = getattr(self, self.COMMAND_CONFIG[command])(message)
        except KeyError:
            self.logger.info("Unknown command passed: %s", command)
        except AttributeError:
            self.logger.error("Attribute not defined for command: %s", command)
        return responses

    def set_connection(self, message: Message) -> ReturnMessage:
        """Sets echo connection to given channel ID if found"""
        try:
            channel_id = int(message.content.split()[1])
        except ValueError:
            return ReturnMessage("", "Invalid channel ID provided")

        self.target_channel = self.client.client.get_channel(channel_id)
        self.target_use_mark = time.perf_counter()

        if not self.target_channel or str(self.target_channel.type) != "text":
            return ReturnMessage("", "Invalid channel or channel-type.")

        return ReturnMessage(
            "",
            (
                f"Target channel set to '{self.target_channel.name}' for the "
                f"next {self.expirey} seconds"
            ),
        )

    def send_echo(self, message: Message) -> ReturnMessage:
        """Ensure we have a target channel that isn't expired"""
        if not self.target_channel:
            return ReturnMessage(
                "", "Use `echo!set [channel ID]` to set a target channel first"
            )

        if (time.perf_counter() - self.target_use_mark) > self.expirey:
            self.target_channel = None
            return ReturnMessage(
                "", "Set channel timed-out. Set again with `echo!set channel [ID]`"
            )

        self.target_use_mark = time.perf_counter()
        return ReturnMessage(
            message.content.replace("echo!send", ""),
            f"Message echo'ed to: {self.target_channel.name}",
        )

    def stop_echo(self, _: Message) -> ReturnMessage:
        """Removes target channel"""
        self.target_channel = None
        self.target_use_mark = 0.0
        return ReturnMessage("", "Echo target cleared.")

    async def on_message(self, msg: Message) -> None:
        """ON MESSAGE event hook"""
        if str(msg.channel.type) != "private" or not self.owner_id:
            return
        self.logger.debug("Got message: %s", msg)
        self.__populate_owner()

        if msg.content.startswith("echo!") and (str(msg.author.id) == self.owner_id):
            result = self.parse_command(msg)
            await self.__send_to_channel(result.channel)
            await self.__send_to_owner(result.owner)
            self.logger.info("Results: %s", result)

        elif self.owner is not None:
            msg = f"EchoBox: DM to bot from {msg.author}\n```{msg.content}```"
            await self.__send_to_owner(msg)
