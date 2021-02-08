#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Egg Bot, Discord Modular Bot

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging

import discord  # type: ignore

from eggbot.configfile import ConfigFile
from eggbot.eventsub import EventSub
from eggbot.utils.loadenv import LoadEnv


logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.members = True
discord_client = discord.Client(status="online", intents=intents)
eventSubs = EventSub()
coreConfig = ConfigFile()
envVars = LoadEnv()


def load_config() -> bool:
    """ Load configuration """
    logger.info("Opening configuration...")
    if not coreConfig.load("./config/eggbot_core.json"):
        logger.warning("Configuration not found!")
        logger.warning("File used: %s", coreConfig.filename)
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


def main() -> int:
    """ Main entry point """
    if not load_config():
        return 1
    envVars.load()
    discord_client.run(envVars.get("DISCORD_TOKEN"))
    return 0


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
