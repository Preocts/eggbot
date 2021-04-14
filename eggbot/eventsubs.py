#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Hold all subscriptions to events from bot addon modules

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
from typing import List
from typing import Protocol
from typing import NamedTuple

from discord import Message  # type: ignore

from eggbot.models.eventtype import EventType


class EventCallback(Protocol):
    """ Protocol duck type """

    async def __call__(self, message: Message) -> None:
        ...


class EventAction(NamedTuple):
    """ Event Action Object """

    event: EventType
    target: EventCallback


class EventSubs:
    """ Hold all subscriptions to events from bot addon modules """

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__pubsub: List[EventAction] = []

    def add(self, event: EventType, target: EventCallback) -> None:
        """ Add new event to event subscriptions """
        self.__pubsub.append(EventAction(event, target))

    def get(self, event: EventType) -> List[EventCallback]:
        """ Returns a list of callable targets by event type, can be empty """
        result: List[EventCallback] = []
        for sub in self.__pubsub:
            if sub.event == event:
                result.append(sub.target)
        return result
