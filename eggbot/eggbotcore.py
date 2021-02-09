#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Egg Bot, Discord Modular Bot

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
from typing import Optional

from eggbot.discordclient import DiscordClient
from eggbot.configfile import ConfigFile
from eggbot.eventsubs import EventSubs
from eggbot.utils.loadenv import LoadEnv
from eggbot.models.eventtype import EventType


class EggBotCore:
    """ Main construct of bot """

    logger = logging.getLogger(__name__)
    event_subs: Optional[EventSubs] = None
    core_config: Optional[ConfigFile] = None
    env_vars: Optional[LoadEnv] = None
    discord_ = DiscordClient()

    def __init__(self) -> None:
        """ Declare class objects """
        self.event_subs = EventSubs()
        self.core_config = ConfigFile()
        self.env_vars = LoadEnv()

    def load_config(self) -> bool:
        """ Load configuration """
        self.logger.info("Opening configuration...")
        if not self.core_config:
            raise Exception("Internal Object 'core_config' not initialized.")
        if not self.core_config.load("./config/eggbot_core.json"):
            self.logger.warning("Configuration not found!")
            self.logger.warning("File used: %s", self.core_config.filename)
            return False
        self.logger.info(
            "Configuration file loaded with %d keys.", len(self.core_config.config)
        )
        return True

    @discord_.client.event
    async def on_member_join(self, member) -> bool:
        """ Triggered on all join events """
        if member.id == self.discord_.client.user.id:
            self.logger.warning("on_member_join(), Saw ourselves join, that's weird.")
            return False
        if member.bot:
            self.logger.info("on_member_join(), Bot join detected, ignoring.")
            return False
        if self.event_subs:
            self.logger.error(self.event_subs.get(EventType.MEMBERJOIN))
            for subbed in self.event_subs.get(EventType.MEMBERJOIN):
                self.logger.error("WE HERE")
                subbed(member)
        return True

    @discord_.client.event
    async def on_message(self, message) -> bool:
        """ Triggered on all message events """
        if message.author.id == self.discord_.client.user.id:
            self.logger.debug("on_message(), Ignoring ourselves.")
            return False
        if message.author.bot:
            self.logger.info("on_message(), Bot chat, ignoring.")
            return False
        if self.event_subs:
            for subbed in self.event_subs.get(EventType.MESSAGE):
                subbed(message)
        return True

    def launch_bot(self) -> int:
        """ Start the bot, blocking """
        if not self.env_vars:
            raise Exception("Internal Object 'env_vars' not initialized.")
        if not self.load_config():
            raise Exception("Unable to load core_configuration.")
        self.env_vars.load()
        self.discord_.set_secret(self.env_vars.get("DISCORD_SECRET"))
        self.discord_.run()
        return 0


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
