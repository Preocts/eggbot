#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Entity objects for the core bot

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging

from typing import Any
from typing import Optional

from eggbot.utils.configio import ConfigIO


class ConfigFile:
    """ Core configuration handler """

    configClient: ConfigIO = ConfigIO()
    logger = logging.getLogger(__name__)

    def __init__(self, filename: Optional[str] = None) -> None:
        """Layer for accessing JSON configuration file

        If the filename is provided the configuration will be loaded and
        load/save methods will reference that file unless a new one is provided.

        Args:
            filename : Path and name of the JSON config file
        """
        self.filename: Optional[str] = filename
        self.__config: dict = {}

    @property
    def config(self) -> dict:
        """ Return copy of configuration dictionary """
        return dict(self.__config)

    def unload(self) -> None:
        """ Unloads config without saving """
        self.__config = {}

    def load(self, filename: Optional[str] = None) -> bool:
        """ Load config. Uses prior loaded file if none provided """
        if filename:
            self.filename = filename
        self.__config = self.configClient.load(self.filename)
        return bool(self.__config)

    def save(self, filename: Optional[str] = None) -> bool:
        """ Save config. Uses prior loaded file if none provided """
        if filename:
            self.filename = filename
        return self.configClient.save(self.__config, self.filename)

    def read(self, key: str) -> Any:
        """ Reads values by key from config. Returns None if not exists """
        return self.__config.get(key)

    def create(self, key: str, value: Any = None) -> bool:
        """ Creates a key/value pair in the configuration """
        if not isinstance(key, str):
            self.logger.error(".create() key not string. Given a %s", str(type(key)))
            return False
        if key in self.config.keys():
            self.logger.error(".create() key already exists, use .update()")
            return False
        self.__config[key] = value
        return True

    def update(self, key: str, value: Any = None) -> bool:
        """ Updates key/value pair in the configuration """
        if key not in self.__config.keys():
            self.logger.error(".update() key not found, use .create()")
            return False
        self.__config[key] = value
        return True

    def delete(self, key: str) -> bool:
        """ Deletes key from configuration """
        if key not in self.__config.keys():
            self.logger.error(".delete() key not found.")
            return False
        del self.__config[key]
        return True
