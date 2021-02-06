#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Egg Bot, Discord Modular Bot

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
import logging

import discord  # type: ignore

from eggbot.configfile import ConfigFile
from eggbot.eventsub import EventSub


DISCORD_TOKEN = os.environ.get("discord_api_key")
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True
discord_client = discord.Client(status="online", intents=intents)
eventSubs = EventSub()
coreConfig = ConfigFile()


def load_config() -> bool:
    """ Load configuration """
    logger.info("Opening configuration...")
    coreConfig.load("./config/eggbot_core.json")
    if not coreConfig.config:
        logger.warning("Configuration not found!")
        # TODO: Add method to pull file path for output
        return False
    logger.info("Configuration file loaded with %d keys.", len(coreConfig.config))
    return True


@discord_client.event
async def on_member_join(member) -> bool:
    """ Triggered on all join events """
    if member.id == discord_client.user.id:
        logger.warning("on_member_join(), Saw ourselves join, that's weird.")
        return False
    if member.bot:
        logger.info("on_member_join(), Bot join detected, ignoring.")
        return False
    for subbed in eventSubs.event_list("on_join"):
        subbed(member)
    return True


@discord_client.event
async def on_message(message) -> bool:
    """ Triggered on all message events """
    if message.author.id == discord_client.user.id:
        logger.debug("on_message(), Ignoring ourselves.")
        return False
    if message.author.bot:
        logger.info("on_message(), Bot chat, ignoring.")
        return False
    for subbed in eventSubs.event_list("on_message"):
        subbed(message)
    return True


def main() -> None:
    """ Main entry point """
    load_config()
    discord_client.run(DISCORD_TOKEN)


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
