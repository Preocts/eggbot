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
        "attr": "set_search",
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
    "sb!unignore": {
        "attr": "unignore",
        "format": "sb!unignore [Name | ID]",
        "help": "Unignores a user by Discord name or ID.",
    },
    "sb!help": {
        "attr": "help",
        "format": "sb!help (command)",
        "help": "Available help: set, on, off, ignore, unignore",
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

    def set_search(self, message: Message) -> str:
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
        self.config.save_config()
        return f"Search set: {segments[1]}"

    def ignore(self, message: Message) -> str:
        """ Add a user to the ignore across all guilds """
        target: str = message.clean_content.replace("sb!ignore", "").strip()
        return self.__ignore_toggle(message, target, True)

    def unignore(self, message: Message) -> str:
        """ Remove a user from ignore across all guilds """
        target: str = message.clean_content.replace("sb!unignore", "").strip()
        return self.__ignore_toggle(message, target, False)

    def __ignore_toggle(self, message: Message, target: str, switch: bool) -> str:
        """ Private method to handle lookup up and changing ignores """
        self.logger.debug("Ignore to %s, '%s'", switch, message.clean_content)
        verb = "added to" if switch else "removed from"
        if not target:
            return f"Error: Formatting. {COMMAND_CONFIG['sb!ignore']['format']}"

        user_id = self.__find_user(target)

        if not user_id:
            return (
                f"'{target}' not found. Use their discord name (not nickname), it "
                "is case sensitive. Or, use their discord ID."
            )

        member_list = self.config.member_list_all(str(message.author.id))
        for config in member_list:
            if switch:
                config.ignore.add(user_id)
            elif user_id in config.ignore:
                config.ignore.remove(user_id)
            self.config.save_member(
                config.guild_id, config.member_id, ignore=config.ignore
            )
        if member_list:
            self.config.save_config()
        return f"'{target}' {verb} ignore list."

    def toggle_on(self, message: Message) -> str:
        """ Toggle ShoulderBird on for message author """
        return self.__toggle(str(message.author.id), True)

    def toggle_off(self, message: Message) -> str:
        """ Toggle ShoulderBird off for message author """
        return self.__toggle(str(message.author.id), False)

    def __toggle(self, member_id: str, switch: bool) -> str:
        """ Private method to handle looking up and changing toggles """
        self.logger.debug("Toggle '%s' to '%s'", member_id, switch)
        verb = "on" if switch else "off"
        member_list = self.config.member_list_all(member_id)
        for member in member_list:
            self.config.save_member(member.guild_id, member.member_id, toggle=switch)
        if member_list:
            self.config.save_config()
            return f"ShoulderBird now **{verb}** for {len(member_list)} guild(s)."

        return "No searches found, use `sb!help set` to get started."

    def __find_guild(self, search: str) -> Optional[str]:
        """ Find guild by ID or name, return None if not found """
        found_id: Optional[str] = None
        for guild in self.discord.guilds:
            if search == str(guild.id) or search == guild.name:
                found_id = str(guild.id)
                break
        return found_id

    def __find_user(self, search: str) -> Optional[str]:
        """ Find member by ID or name, return None if not found """
        found_id: Optional[str] = None
        for user in self.discord.users:
            if search == str(user.id) or search == user.name:
                found_id = str(user.id)
                break
        return found_id

    def help(self, message: Message) -> str:
        """ Helpful help is always helpful """
        self.logger.debug("Help: %s", message.clean_content)
        target = "sb!" + message.clean_content.replace("sb!help", "").strip()
        if target not in COMMAND_CONFIG:
            target = "sb!help"

        return "\n".join(
            [
                COMMAND_CONFIG[target]["help"],
                f"`{COMMAND_CONFIG[target]['format']}`",
            ]
        )
