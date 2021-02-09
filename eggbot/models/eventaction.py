#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Datatype defining a single event and target action

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from typing import Callable

from eggbot.models.eventtype import EventType


class EventAction:
    """ Datatype defining a single event and target action """

    def __init__(self, event: EventType, target: Callable) -> None:
        """ Define an event with callable target """
        self.__event = event
        self.__target = target

    @property
    def event(self) -> EventType:
        """ Anchor Event """
        return self.__event

    @property
    def target(self) -> Callable:
        """ Callable target """
        return self.__target
