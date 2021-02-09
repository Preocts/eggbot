#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Hold all subscriptions to events from bot addon modules

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging

from typing import List
from typing import Callable

from eggbot.models.eventaction import EventAction
from eggbot.models.eventtype import EventType


class EventSubs:
    """ Hold all subscriptions to events from bot addon modules """

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__pubsub: List[EventAction] = []

    def add(self, event: EventType, target: Callable) -> None:
        """ Add new event to event subscriptions """
        self.__pubsub.append(EventAction(event, target))

    def get(self, event: EventType) -> List[Callable]:
        """ Returns a list of callable targets by event type, can be empty """
        result: List[Callable] = []
        for sub in self.__pubsub:
            if sub.event == event:
                result.append(sub.target)
        return result
