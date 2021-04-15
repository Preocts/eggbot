#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shoulder Bird is a bot plugin that pings a user when a defined keyword is read in chat

The objects in this script are the layer for CRUD operations against ShoulderBird's
configuration file.  If the file is missing a new one will be created.  Each config
contains top-level key-values for the module name and version which can be used
to upgrade existing configs when schema changes.

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
from typing import Set
from typing import List

from eggbot.configfile import ConfigFile

MODULE_NAME = "ShoulderBird"
MODULE_VERSION = "1.0.0"
DEFAULT_CONFIG = "configs/shoulderbird.json"


class BirdMember:
    """ Model class for member level config values """

    # pylint: disable=too-few-public-methods

    def __init__(self, guild_id: str, member_id: str, **kwargs) -> None:
        self.guild_id = guild_id
        self.member_id = member_id
        self.regex: str = kwargs.get("regex", "")
        self.toggle: bool = kwargs.get("toggle", True)
        self.ignore: Set[str] = set(kwargs.get("ignore", []))

    def to_dict(self) -> dict:
        """ Converts values to dict for use in JSON """
        return {
            "guild_id": self.guild_id,
            "member_id": self.member_id,
            "regex": self.regex,
            "toggle": self.toggle,
            "ignore": list(self.ignore),
        }


class ShoulderBirdConfig:
    """ Shoulder Bird Config class, CRUD config operations """

    logger = logging.getLogger(__name__)

    def __init__(self, config_file: str = DEFAULT_CONFIG) -> None:
        """ Init and load config """
        self.logger.info("Initializing Shoulder Bird Parser")
        self.__configclient = ConfigFile()
        self.__configclient.load(config_file)
        if not self.__configclient.config:
            self.__configclient.create("module", MODULE_NAME)
            self.__configclient.create("version", MODULE_VERSION)

    def __load_guild(self, guild_id: str) -> dict:
        """ Load a specific guild from config. Will create guild if not found """
        self.logger.debug("load_guild: '%s'", guild_id)
        if guild_id not in self.__configclient.config:
            self.__configclient.create(guild_id, {})
        return self.__configclient.read(guild_id)

    def __save_member_to_guild(self, guild_id: str, member: BirdMember) -> None:
        """ Save a specific member to a guild. Creates new or overwrites existing """
        guild_config = self.__load_guild(guild_id)
        guild_config[member.member_id] = member.to_dict()
        self.__configclient.update(guild_id, guild_config)

    def reload_config(self) -> bool:
        """ Reloads current config file without saving """
        return self.__configclient.load()

    def save_config(self) -> bool:
        """ Saves current config to file """
        return self.__configclient.save()

    def member_list_all(self, member_id: str) -> List[BirdMember]:
        """ Returns all configs for member across guilds, can return empty list """
        self.logger.debug("member_list_all: '%s'", member_id)
        config_list = []
        for guild in self.__configclient.config.values():
            if member_id in guild:
                config_list.append(BirdMember(**guild[member_id]))
        return config_list

    def guild_list_all(self, guild_id: str) -> List[BirdMember]:
        """ Returns all configs within a single guild, can return empty list """
        self.logger.debug("guild_list_all: '%s'", guild_id)
        config_list = []
        for member in self.__load_guild(guild_id).values():
            config_list.append(BirdMember(**member))
        return config_list

    def load_member(self, guild_id: str, member_id: str) -> BirdMember:
        """ Load a member from a guild. Will return empty member if not found """
        self.logger.debug("load_member: '%s', '%s'", guild_id, member_id)
        member = self.__load_guild(guild_id).get(member_id)
        return BirdMember(**member) if member else BirdMember(guild_id, member_id)

    def save_member(self, guild_id: str, member_id: str, **kwargs) -> BirdMember:
        """Save (creating or updating) a member to a guild

        Keyword Args:
            regex [str] : Regular expression
            toggle [bool] : True if config is active, False if inactive
            ignore Set[str] : Set of member IDs to ignore. Can be empty
        """
        self.logger.debug("save_member: '%s', '%s', '%s'", guild_id, member_id, kwargs)
        member_config = self.load_member(guild_id, member_id)
        member_config.regex = kwargs.get("regex", member_config.regex)
        member_config.toggle = kwargs.get("toggle", member_config.toggle)
        member_config.ignore = kwargs.get("ignore", member_config.ignore)
        self.__save_member_to_guild(guild_id, member_config)
        return member_config

    def delete_member(self, guild_id: str, member_id: str) -> bool:
        """ Deletes member from specific guild, returns false if not found """
        self.logger.debug("delete_member: '%s', '%s'", guild_id, member_id)
        guild_config = self.__load_guild(guild_id)
        deleted_value = guild_config.pop(member_id, None)
        if deleted_value:
            self.__configclient.update(guild_id, guild_config)
        return bool(deleted_value)
