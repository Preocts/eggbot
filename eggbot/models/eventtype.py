#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Abstract for supported event types

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from enum import Enum


class EventType(Enum):
    """ Abstract for supported event types """

    READY = 0
    DISCONNECT = 1
    MEMBERJOIN = 2
    MESSAGE = 3
