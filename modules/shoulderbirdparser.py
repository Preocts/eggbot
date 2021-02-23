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
from __future__ import annotations

import re
import time
import logging
from typing import List

from eggbot.discordclient import DiscordClient
from modules.shoulderbirdconfig import DEFAULT_CONFIG
from modules.shoulderbirdconfig import BirdMember
from modules.shoulderbirdconfig import ShoulderBirdConfig


class ShoulderBirdParser:
    """ Point of entry object for ShoulderBird module """

    logger = logging.getLogger(__name__)

    def __init__(self, config_file: str = DEFAULT_CONFIG) -> None:
        """ Loads config """
        self.__config = ShoulderBirdConfig(config_file)

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
            if re.search(fr"(?i)\b{member.regex}\b", clean_message):
                self.logger.debug("Match found: '%s'", member.member_id)
                match_list.append(member)
        return match_list

    async def onmessage(self, discord_message: DiscordClient.message) -> None:
        """ Hook for discord client, async coro """
        tic = time.perf_counter()
        self.logger.info("[START] onmessage")
        message = SimpleMessage(discord_message)
        guild: DiscordClient.guild = discord_message.guild

        if not message.content or not message.is_text_channel():
            self.logger.info("Unsupported channel or empty message.")
            return None
        matches = self.get_matches(message.guild_id, message.user_id, message.content)

        for match in matches:
            if match.member_id not in message.get_channel_member_ids():
                self.logger.debug(
                    "'%s' not in channel '%s'", match.member_id, message.channel_name
                )
                continue
            self.__send_dm(match, message, guild)

        self.logger.info(
            "[FINISH] onmessage completed: %f ms", round(time.perf_counter() - tic, 2)
        )

    async def __send_dm(
        self, member: BirdMember, message: SimpleMessage, guild: DiscordClient.guild
    ) -> None:
        """ Private - send DM message to match. To be replaced with actions queue """
        try:
            target: DiscordClient.member = guild.get_member(int(member.member_id))
        except ValueError:
            self.logger.error(
                "Invalid member_id conversion to int: '%s'", member.member_id
            )
            target = None
        if target:
            msg = (
                f"ShoulderBird notification, **{message.author}** mentioned you in "
                "**{message.channel_name}** saying:\n`{message.content}`"
            )
            await target.dm_channel.send(msg)


class SimpleMessage:
    """ Data-type class for simplifing discord message object """

    def __init__(self, message: DiscordClient.message) -> None:
        """ Data-type class for simplifing discord message object """
        self.__message = message
        self.content: str = message.clean_content
        self.channel_name: str = message.channel.name
        self.guild_id: str = str(message.guild.id)
        self.user_id: str = str(message.author.id)
        self.author: str = message.author.display_name

    def get_channel_member_ids(self) -> List[str]:
        """ Returns list of member_ids in message channel, can return empty """
        id_list: List[str] = []
        if self.is_text_channel():
            id_list = [str(member.id) for member in self.__message.channel.members]
        return id_list

    def is_text_channel(self) -> bool:
        """ Bool flag for channel type """
        return self.__message.channel.type == "text"
