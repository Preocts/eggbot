#!/usr/bin/env python3
""" Abstract for supported event types

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from enum import Enum


class EventType(Enum):
    """ Abstract for supported event types """

    ON_READY = 0
    ON_DISCONNECT = 1
    ON_MEMBER_JOIN = 2
    ON_MESSAGE = 3
