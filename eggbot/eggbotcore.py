#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Egg Bot, Discord Modular Bot

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import importlib
import logging
import os
import sys
from typing import List

from discord import Member
from discord import Message

from eggbot.configfile import ConfigFile
from eggbot.discordclient import DiscordClient
from eggbot.eventsubs import EventSubs
from eggbot.models.eventtype import EventType
from eggbot.utils.loadenv import LoadEnv


class EggBotCore:
    """Main construct of bot"""

    DEFAULT_CONFIG = "configs/eggbotcore.json"
    MODULE_PATH = "./modules"

    logger = logging.getLogger(__name__)
    discord_ = DiscordClient()

    def __init__(self) -> None:
        """Declare class objects"""
        self.event_subs = EventSubs()
        self.core_config = ConfigFile()
        self.env_vars = LoadEnv()
        self.loaded_modules: List[object] = []

    def load_config(self) -> bool:
        """Load configuration"""
        self.logger.info("Opening configuration...")
        if not self.core_config:
            raise Exception("Internal Object 'core_config' not initialized.")
        if not self.core_config.load(self.DEFAULT_CONFIG):
            self.logger.warning("Configuration not found!")
            self.logger.warning("File used: %s", self.core_config.filename)
            return False
        self.logger.info(
            "Configuration file loaded with %d keys.", len(self.core_config.config)
        )
        return True

    async def on_member_join(self, member: Member) -> bool:
        """Triggered on all join events"""
        if member.id == self.discord_.client.user.id:
            self.logger.warning("on_member_join(), Saw ourselves join, that's weird.")
            return False
        if member.bot:
            self.logger.info("on_member_join(), Bot join detected, ignoring.")
            return False
        if self.event_subs:
            for subbed in self.event_subs.get(EventType.ON_MEMBER_JOIN):
                await subbed(member)
        return True

    async def on_message(self, message: Message) -> bool:
        """Triggered on all message events"""
        if message.author.id == self.discord_.client.user.id:
            self.logger.debug("on_message(), Ignoring ourselves.")
            return False
        if message.author.bot:
            self.logger.info("on_message(), Bot chat, ignoring.")
            return False
        if str(message.author.id) == self.env_vars.get("BOT_OWNER"):
            if message.content == "egg!dc":
                await self.discord_.close()
                return False
        if self.event_subs:
            for subbed in self.event_subs.get(EventType.ON_MESSAGE):
                await subbed(message)
        return True

    async def on_ready(self) -> bool:
        """Triggered when client has completed processing of data recieved"""
        if self.event_subs:
            for subbed in self.event_subs.get(EventType.ON_READY):
                await subbed(None)
        return True

    async def on_disconnect(self) -> bool:
        """Triggered on disconnect. Does not indicate re-connect logic will fail"""
        if self.event_subs:
            for subbed in self.event_subs.get(EventType.ON_DISCONNECT):
                await subbed(None)
        return True

    def launch_bot(self) -> int:
        """Start the bot, blocking"""
        self.__load_environment()
        self.__load_modules()
        self.__register_events()
        self.discord_.run()
        return 0

    def __load_environment(self) -> None:
        """Load core config and environment variables"""
        if not self.env_vars:
            raise Exception("Internal Object 'env_vars' not initialized.")
        if not self.load_config():
            raise Exception("Unable to load core_configuration.")
        self.env_vars.load()
        self.discord_.set_secret(self.env_vars.get("DISCORD_SECRET"))

    def __register_events(self) -> None:
        """Link event handler methods to discord client"""
        # This replaces the @discord.client.event decorators as we want to
        # capture the instance method of these, not the unbound function.
        self.discord_.client.event(self.on_ready)
        self.discord_.client.event(self.on_disconnect)
        self.discord_.client.event(self.on_member_join)
        self.discord_.client.event(self.on_message)

    def __load_modules(self) -> None:
        """Load the modules for the bot"""
        for module_name in self.__get_module_files():
            if module_name in sys.modules:
                continue
            try:
                module = importlib.import_module(f"modules.{module_name}")
                self.__register_module_events(module, module_name)
            except ModuleNotFoundError as err:
                self.logger.error("Module not loaded: '%s' (%s)", module_name, err)

    def __get_module_files(self) -> List[str]:
        """Returns list of ./modules/module*.py files"""
        file_list: List[str] = []
        for result in os.listdir(self.MODULE_PATH):
            if result.startswith("module_") and result.endswith(".py"):
                file_list.append(result[:-3])
        return file_list

    def __register_module_events(self, module: object, module_name: str) -> None:
        """Initializes module class and registers identified event subscriptions"""
        class_name = getattr(module, "AUTO_LOAD", None)
        if class_name is None:
            raise ModuleNotFoundError("Unable to find expected AUTO_LOAD attr")

        class_attr = getattr(sys.modules[f"modules.{module_name}"], class_name, None)
        if class_attr is None:
            raise ModuleNotFoundError(f"Unable to find class name: {class_name}")

        self.loaded_modules.append(class_attr())

        for event in EventType:
            callback = getattr(self.loaded_modules[-1], event.name.lower(), None)
            if not callback:
                continue
            self.logger.info("Registering %s for %s", module_name, event.name.lower())
            self.event_subs.add(event, callback)


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
