#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Abstract layer for discord client library

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from __future__ import annotations

from typing import Optional

import discord  # type: ignore


class SingleClient(type):
    """ Python singleton factory """

    _instances: Optional[discord.Client] = None

    def __call__(cls):
        """ Provide existing instance or create one """
        if not cls._instances:
            cls._instances = super(SingleClient, cls).__call__()
        return cls._instances


class DiscordClient(metaclass=SingleClient):
    """ Abstract layer for discord client of choice """

    def __init__(self) -> None:
        self.__discord_secret = ""
        intents = discord.Intents.default()
        intents.members = True
        self.client = discord.Client(status="online", intents=intents)

    def set_secret(self, discord_secret: str) -> None:
        """ Store Discord API key """
        self.__discord_secret = discord_secret

    def run(self) -> None:
        """ Start discord connection - blocking """
        self.client.run(self.__discord_secret)
