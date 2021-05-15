#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Hold all subscriptions to events from bot addon modules

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
from typing import Any
from typing import Callable
from typing import Coroutine
from typing import List
from typing import NamedTuple

from eggbot.models.eventtype import EventType

EVENTCALLBACK = Callable[[Any], Coroutine[Any, Any, None]]


class EventAction(NamedTuple):
    """ Event Action Object """

    event: EventType
    target: EVENTCALLBACK


class EventSubs:
    """ Hold all subscriptions to events from bot addon modules """

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__pubsub: List[EventAction] = []

    def add(self, event: EventType, target: EVENTCALLBACK) -> None:
        """ Add new event to event subscriptions """
        self.__pubsub.append(EventAction(event, target))

    def get(self, event: EventType) -> List[EVENTCALLBACK]:
        """ Returns a list of callable targets by event type, can be empty """
        result: List[EVENTCALLBACK] = []
        for sub in self.__pubsub:
            if sub.event == event:
                result.append(sub.target)
        return result
