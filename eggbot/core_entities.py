# -*- coding: utf-8 -*-
""" Entity objects for the core bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from __future__ import annotations

import json
import os
import logging
import pathlib

from typing import Any
from typing import Callable
from typing import Optional

import dotenv


logger = logging.getLogger(__name__)
dotenv.load_dotenv()


class CoreConfig:
    """ Core configuration handler, singleton class """

    __core_config: Optional[CoreConfig] = None

    @staticmethod
    def get_instance() -> CoreConfig:
        """ Get instance of singleton class """
        if not CoreConfig.__core_config:
            CoreConfig()
        return CoreConfig.__core_config

    def __init__(self):
        if CoreConfig.__core_config:
            raise Exception("Singleton class. Use .get_instance() instead")
        self.__abs_path = f"{os.path.sep}".join(
            __file__.split(os.path.sep)[0:-2]
        )
        self.__cwd = os.getcwd()
        self.__config = {}
        CoreConfig.__core_config = self

    @property
    def abs_path(self) -> str:
        return self.__abs_path

    @property
    def cwd(self) -> str:
        return self.__cwd

    @property
    def config(self) -> dict:
        return dict(self.__config)

    def load(
        self,
        filepath: str = "./config/eggbot_core.json",
        abs_path: bool = False,
    ) -> bool:
        """Loads a config json

        Args:
            filepath: If provided this will override loading the default
                configuration file expected at './config/eggbot.json'
            abs_path: If True the filepath provided is treated as an
                absolute path. Otherwise the path is considered
                relative to this module
        """
        self.__config = {}
        rel_path = pathlib.Path(self.cwd).joinpath(filepath)
        path = filepath if abs_path else rel_path.resolve()

        try:
            with open(path, "r") as input_file:
                self.__config = json.loads(input_file.read())

        except (FileNotFoundError, IsADirectoryError):
            logger.error(f".load() Configuration file not found at: {path}")

        except json.decoder.JSONDecodeError:
            logger.error(
                ".load() Configuration file empty or formatted "
                "incorrectly, that's sad. You can get a new one "
                "over at: https://github.com/Preocts/Egg_Bot"
            )
            return False

        except (OSError, Exception):
            logger.error(
                ".load() Something went wrong loading configuations..."
            )
            logger.error("", exc_info=True)
            return False

        return True

    def save(
        self,
        filepath: str = "./config/eggbot_core.json",
        abs_path: bool = False,
    ) -> bool:
        """Saves a config json

        !Destructive save! Will not prevent overwriting existing files.

        Args:
            filepath: If provided this will override loading the default
                configuration file expected at './config/eggbot.json'
            abs_path: If True the filepath provided is treated as an
                absolute path. Otherwise the path is considered
                relative to this module
        """
        rel_path = pathlib.Path(self.cwd).joinpath(filepath)
        path = filepath if abs_path else rel_path.resolve()
        try:
            with open(path, "w") as out_file:
                out_file.write(json.dumps(self.__config, indent=4))
        except Exception as err:
            logger.error(f".save() Cannot save core config: {err}")
            logger.error("", exc_info=True)
            return False
        return True

    def unload(self) -> None:
        """ Unloads config without saving """
        self.__config = {}

    def read(self, key: str) -> Any:
        """ Reads values by key from config. Returns None if not exists """
        return self.__config.get(key)

    def create(self, key: str, value: Any = None) -> bool:
        """ Creates a key/value pair in the configuration """
        if not isinstance(key, str):
            logger.error(f".create() key not string. Given a {type(key)}")
            return False
        if key in self.config.keys():
            logger.error(".create() key already exists, use .update()")
            return False
        self.__config[key] = value
        return True

    def update(self, key: str, value: Any = None) -> bool:
        """ Updates key/value pair in the configuration """
        if key not in self.__config.keys():
            logger.error(".update() key not found, use .create()")
            return False
        self.__config[key] = value
        return True

    def delete(self, key: str) -> bool:
        """ Deletes key from configuration """
        if key not in self.__config.keys():
            logger.error(".delete() key not found.")
            return False
        del self.__config[key]
        return True


class EventSub(object):
    """Allows modules to sub to event notifications

    A component to the pub/sub framework for how the bot handles events
    and allows future scalability. Declare one EventSub() object per
    bot instance. Multiple declared instances can be used but do not
    provide additional control or function.
    """

    def __init__(self):
        self._pubsub = {}

    def sub_create(self, target: Callable, event: str) -> bool:
        """Subscribe a target to an event

        Args:
            target - The target callable object
            event - The name of the event group to be subbed

        Returns:
            Bool - False if failed to create (check logs)
        """
        if not isinstance(target, Callable):
            logger.error(f".sub(), [target] is not callable: {type(target)}")
            return False

        if not self._pubsub.get(event):
            self._pubsub[event] = set()  # Ensure we have a key

        if target in self._pubsub[event]:
            logger.error(".sub(), [target] already subscribed")
            return False

        self._pubsub[event].add(target)

        return True

    def sub_delete(self, target: callable, event: str) -> bool:
        """Unsubscribe a target from an event

        Args:
            target - The target callable object
            event - The name of the event group to be unsubbed

        Returns:
            Bool - False if failed to unsub (check logs)
        """
        if not self._pubsub.get(event):
            logger.error(f".unsub(), Event '{event}' does not exist.")
            return False

        if target not in self._pubsub[event]:
            logger.error(f".unsub(), [target] is not subbed to '{event}'")
            return False

        self._pubsub[event].remove(target)

        return True

    def sub_wipe(self, target: callable) -> bool:
        """Removes target from all subscriptions

        Args:
            target - The target callable object to be removed

        Returns:
            True
        """
        events = self.event_list_all()

        for event in events:
            self._pubsub[event].discard(target)

        return True

    def sub_list(self, target: callable) -> tuple:
        """ Returns a list of events that target is subbed to """
        sub_list = []
        for event in self.event_list_all():
            if target in self._pubsub[event]:
                sub_list.append(event)
        return tuple(sub_list)

    def event_list_all(self) -> tuple:
        """ Returns tuple of all events """
        return tuple(self._pubsub.keys())

    def event_list(self, event: str) -> tuple:
        """ Returns all subscribed callables in event """
        if event not in self._pubsub.keys():
            logger.warning(f'event_list(), Event "{event}" not found.')
        return tuple(self._pubsub.get(event, ()))

    def event_delete(self, event: str) -> bool:
        """ Deletes an entire event, unsubbing all within """
        if event not in self._pubsub.keys():
            logger.error(f'event_delete(), Event "{event}" not found.')
            return False
        del self._pubsub[event]
        return True

    def event_create(self, event: str) -> bool:
        """ Creates an empty event set """
        if event in self._pubsub.keys():
            return False
        self._pubsub[event] = set()
        return True
