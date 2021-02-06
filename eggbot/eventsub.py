#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Hold all subscriptions to events from bot addons

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging

from typing import Callable


class EventSub:
    """Allows modules to sub to event notifications

    A component to the pub/sub framework for how the bot handles events
    and allows future scalability. Declare one EventSub() object per
    bot instance. Multiple declared instances can be used but do not
    provide additional control or function.
    """

    logger = logging.getLogger(__name__)

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
        if not self._pubsub.get(event):
            self._pubsub[event] = set()  # Ensure we have a key

        if target in self._pubsub[event]:
            self.logger.error(".sub(), [target] already subscribed")
            return False

        self._pubsub[event].add(target)

        return True

    def sub_delete(self, target: Callable, event: str) -> bool:
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

    def sub_wipe(self, target: Callable) -> bool:
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

    def sub_list(self, target: Callable) -> tuple:
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
            self.logger.warning("event_list(), Event '%s' not found.", event)
        return tuple(self._pubsub.get(event, ()))

    def event_delete(self, event: str) -> bool:
        """ Deletes an entire event, unsubbing all within """
        if event not in self._pubsub.keys():
            self.logger.error("event_delete(), Event '%s' not found.", event)
            return False
        del self._pubsub[event]
        return True

    def event_create(self, event: str) -> bool:
        """ Creates an empty event set """
        if event in self._pubsub.keys():
            return False
        self._pubsub[event] = set()
        return True
