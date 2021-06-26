#!/usr/bin/env python3
""" Abstract layer for discord client library

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from __future__ import annotations

from typing import Any
from typing import List
from typing import Optional

import discord


class SingleClient(type):
    """Python singleton factory"""

    _instances: Optional[discord.Client] = None

    def __call__(cls) -> Any:  # type: ignore
        """Provide existing instance or create one"""
        if not cls._instances:
            cls._instances = super(SingleClient, cls).__call__()
        return cls._instances


class DiscordClient(metaclass=SingleClient):
    """Abstract layer for discord client of choice"""

    def __init__(self) -> None:
        """Creates a singleon of a Discord Client"""
        self.__discord_secret = ""
        intents = discord.Intents(messages=True, guilds=True, members=True)
        self.client = discord.Client(status="online", intents=intents)

    def set_secret(self, discord_secret: str) -> None:
        """Store Discord API key"""
        self.__discord_secret = discord_secret

    def run(self) -> None:
        """Start discord connection - blocking"""
        self.client.run(self.__discord_secret)

    async def close(self) -> None:
        """Shut down the connection"""
        await self.client.close()

    @property
    def guilds(self) -> List[discord.Guild]:
        """List of guilds loaded to client"""
        return self.client.guilds

    @property
    def users(self) -> List[discord.User]:
        """List of users loaded to client"""
        return self.client.users
