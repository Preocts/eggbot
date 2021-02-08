#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Hold all subscriptions to events from bot addon modules

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
import logging
import importlib

from typing import Callable


class EventSub:
    """
    Allows modules to sub to event notifications

    A component to the pub/sub framework for how the bot handles events
    and allows future scalability. Declare one EventSub() object per
    bot instance. Multiple declared instances can be used but do not
    provide additional control or function.
    """

    logger = logging.getLogger(__name__)

    def __init__(self):
        self._pubsub = {}

    def load_modules(self) -> bool:
        """ loads modules from module directory and creates events """
        if not os.path.isdir("./modules"):
            return False
        for file_ in os.listdir("./modules"):
            if file_.endswith(".py") and (file_.startswith("module_")):
                importlib.import_module("modules." + file_[:-3])
                self.logger.info("Loaded module: %s", file_)
                # (sys.modules["eggbot.modules." + mod].initClass())
        return True

    def create(self, target: Callable, event: str) -> bool:
        """Subscribe a target to an event

        Args:
            target - The target callable object
            event - The name of the event group to be subbed

        Returns:
            Bool - False if failed to create (check logs)
        """
        if not self._pubsub.get(event):
            self._pubsub[event] = set()  # Ensure we have a key

        if target in self._pubsub[event]:
            self.logger.error(".sub(), [target] already subscribed")
            return False

        self._pubsub[event].add(target)

        return True

    def delete(self, target: Callable, event: str) -> bool:
        """Unsubscribe a target from an event

        Args:
            target - The target callable object
            event - The name of the event group to be unsubbed

        Returns:
            Bool - False if failed to unsub (check logs)
        """
        if not self._pubsub.get(event):
            self.logger.error(".unsub(), Event '%s' does not exist.", event)
            return False

        if target not in self._pubsub[event]:
            self.logger.error(".unsub(), [target] is not subbed to '%s'", event)
            return False

        self._pubsub[event].remove(target)

        return True

    def event_list(self, event: str) -> tuple:
        """ Returns all subscribed callables in event """
        if event not in self._pubsub.keys():
            self.logger.warning("event_list(), Event '%s' not found.", event)
        return tuple(self._pubsub.get(event, ()))
