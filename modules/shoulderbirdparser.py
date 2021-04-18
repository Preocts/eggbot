#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shoulder Bird is a bot plugin that pings a user when a defined keyword is read in chat

This was designed for Nayomii.

The processes contained in this script handle parsing chat messages to identify
keywords as defined on a guild/user basis. Keywords are searched by word bounded
regex expressions. When a keyword is found, the contents of the message containing
the keyword is send, via DM, to the user who setup the search.

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import re
import time
import logging
from typing import List

from discord import Message  # type: ignore
from discord import Guild  # type: ignore
from discord import Member  # type: ignore

from modules.shoulderbirdconfig import DEFAULT_CONFIG
from modules.shoulderbirdconfig import BirdMember
from modules.shoulderbirdconfig import ShoulderBirdConfig
from modules.shoulderbirdcli import ShoulderbirdCLI


class ShoulderBirdParser:
    """ Point of entry object for ShoulderBird module """

    logger = logging.getLogger(__name__)

    def __init__(self, config_file: str = DEFAULT_CONFIG) -> None:
        """ Loads config """
        self.__config = ShoulderBirdConfig(config_file)
        self.cli = ShoulderbirdCLI(self.__config)

    def close(self):
        """ Saves config state, breaks all references """
        self.__config.save_config()
        del self.__config

    def get_matches(
        self, guild_id: str, user_id: str, clean_message: str
    ) -> List[BirdMember]:
        """ Returns a list of BirdMembers whos searches match clean_message """
        self.logger.debug(
            "get_matches: '%s', '%s', '%s'", guild_id, user_id, clean_message
        )
        match_list: List[BirdMember] = []
        guild_members = self.__config.guild_list_all(guild_id)
        for member in guild_members:
            if not (member.toggle and member.regex) or user_id in member.ignore:
                continue
            # Word bound regex search, case agnostic
            if re.search(fr"(?i)\b({member.regex})\b", clean_message):
                self.logger.debug("Match found: '%s'", member.member_id)
                match_list.append(member)
        return match_list

    @classmethod
    def __is_valid_message(cls, message: Message) -> bool:
        """ Tests for valid message to process """
        if not isinstance(message, Message):
            cls.logger.error("Unknown arg type: %s", type(message))
            return False

        if not message.content:
            cls.logger.debug("Empty message given, skipping.")
            return False

        if str(message.channel.type) not in ["text", "private"]:
            cls.logger.debug("Unsupported message type, skipping.")
            return False

        return True

    async def onmessage(self, message: Message) -> None:
        """ Hook for discord client, async coro """
        if not ShoulderBirdParser.__is_valid_message(message):
            return None

        tic = time.perf_counter()
        self.logger.debug("[START] onmessage")

        # If this is a private message, branch to CLI hander and return here
        if str(message.channel.type) == "private":
            response = self.cli.parse_command(message)
            if response:
                await self.__send_dm(message.author, response)
            return None

        guild: Guild = message.guild
        channel_ids: List[str] = [str(member.id) for member in message.channel.members]

        matches = self.get_matches(
            str(message.guild.id), str(message.author.id), message.content
        )

        for match in matches:
            if match.member_id not in channel_ids:
                self.logger.debug(
                    "'%s' not in channel '%s'", match.member_id, message.channel_name
                )
                continue
            await self.__send_match_dm(match, message, guild)

        self.logger.debug(
            "[FINISH] onmessage completed: %f ms", round(time.perf_counter() - tic, 2)
        )

    async def __send_match_dm(
        self, member: BirdMember, message: Message, guild: Guild
    ) -> None:
        """ Private - send DM message to match. To be replaced with actions queue """
        try:
            target: Member = guild.get_member(int(member.member_id))
        except ValueError:
            self.logger.error("Invalid member_id to int: '%s'", member.member_id)
            return

        msg = (
            f"ShoulderBird notification, **{message.author.display_name}** "
            f"mentioned you in **{message.channel.name}** saying:\n"
            f"`{message.clean_content}`\n{message.jump_url}"
        )
        await self.__send_dm(target, msg)

    @staticmethod
    async def __send_dm(target: Member, content: str) -> None:
        """ Private, sends a DM to target """
        if target.dm_channel is None:
            await target.create_dm()
        if target.dm_channel:
            await target.dm_channel.send(content)


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
