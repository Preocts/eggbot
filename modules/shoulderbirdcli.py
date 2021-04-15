#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shoulder Bird is a bot plugin that pings a user when a defined keyword is read in chat

This was designed for Nayomii.

This class file handle the DM controlled commands for Shoulderbird. The
goal is to allow full configuration of the module from the DM window
within Discord.

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
from typing import Dict
from typing import List
from typing import Optional

from discord import Message  # type: ignore

from eggbot.discordclient import DiscordClient
from modules.shoulderbirdconfig import ShoulderBirdConfig

COMMAND_CONFIG: Dict[str, Dict[str, str]] = {
    "sb!set": {
        "attr": "set",
        "format": "sb!set [Guild Name | Guild ID] = [keyword]",
        "help": "Sets keyword search for a specific guild.",
    },
    "sb!on": {
        "attr": "toggle_on",
        "format": "sb!on",
        "help": "Turns ShoulderBird alerts on.",
    },
    "sb!off": {
        "attr": "toggle_off",
        "format": "sb!off",
        "help": "Turns ShoulderBird alerts off.",
    },
    "sb!ignore": {
        "attr": "ignore",
        "format": "sb!ignore [Name | ID]",
        "help": "Ignores a user by Discord name or ID.",
    },
}


class ShoulderbirdCLI:
    """ Shoulderbird command line via direct messages """

    logger = logging.getLogger(__name__)

    def __init__(self, config: ShoulderBirdConfig) -> None:
        """ Initialize to loaded config """
        self.config = config
        self.discord = DiscordClient()  # Guild list lookup

    def parse_command(self, message: Message) -> Optional[str]:
        """ Parse incoming command, return any response to message """
        return_value: Optional[str] = None
        if not message.clean_content.startswith("sb!"):
            self.logger.debug("Not a command.")
            return return_value
        command = message.clean_content.split()[0]
        try:
            target = getattr(self, COMMAND_CONFIG[command]["attr"])
        except KeyError:
            self.logger.debug("Command not found, %s", command)
            return return_value
        except AttributeError:
            self.logger.error("Command method not found, %s", command)
            return return_value

        return_value = target(message)

        return return_value

    def set(self, message: Message) -> str:
        """ Set a search """
        self.logger.debug("Set search, '%s'", message.clean_content)
        segments: List[str] = message.clean_content.replace("sb!set ", "").split("=", 1)
        if len(segments) != 2 or not segments[1].strip():
            return f"Error: Formatting. {COMMAND_CONFIG['sb!set']['format']}"
        guild_id = self.__find_guild(segments[0].strip())

        if guild_id is None:
            return f"Error: Guild not found, {segments[0].strip()}"

        self.config.save_member(
            guild_id, str(message.author.id), regex=segments[1].strip()
        )

        return f"Search set: {segments[1]}"

    def __find_guild(self, guild_id: str) -> Optional[str]:
        """ Find guild by ID or name, return None if not found """
        found_id: Optional[str] = None
        for guild in self.discord.guilds:
            if guild_id == str(guild.id) or guild_id == guild.name:
                found_id = str(guild.id)
                break
        return found_id
