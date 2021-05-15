# -*- coding: utf-8 -*-
""" Unit Tests

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import unittest

from eggbot.eventsubs import EventSubs
from eggbot.models.eventtype import EventType


class TestEventSub(unittest.TestCase):
    """Test Suite"""

    def test_create_and_get_events(self):
        """Manual add and get"""
        events_client = EventSubs()
        mockclass = MockClass()

        events_client.add(EventType.ON_MEMBER_JOIN, mockclass.method01)  # type: ignore
        events_client.add(EventType.ON_DISCONNECT, mockclass.method02)  # type: ignore
        events_client.add(EventType.ON_MESSAGE, mockfunc)  # type: ignore

        self.assertEqual(
            type(events_client.get(EventType.ON_MEMBER_JOIN)[0]),
            type(mockclass.method01),
        )
        self.assertEqual(
            type(events_client.get(EventType.ON_DISCONNECT)[0]),
            type(mockclass.method02),
        )
        self.assertEqual(
            type(events_client.get(EventType.ON_MESSAGE)[0]), type(mockfunc)
        )


class MockClass:
    """Mock class for mock test"""

    def __init__(self) -> None:
        """Mock"""
        self.ran = False

    def method01(self) -> None:
        """Mock"""
        self.ran = True

    def method02(self) -> None:
        """Mock"""
        self.ran = True


def mockfunc() -> None:
    """Mock"""
