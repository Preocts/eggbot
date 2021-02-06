# -*- coding: utf-8 -*-
""" Unit Tests

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
import unittest

from eggbot.eventsub import EventSub


logger = logging.getLogger(__name__)


class TestEventSub(unittest.TestCase):
    """ Test Suite """

    def test_object_methods(self):
        """ Ensure expected attributes """
        expected_methods = [
            "sub_create",
            "sub_delete",
            "sub_wipe",
            "sub_list",
            "event_create",
            "event_delete",
            "event_list",
            "event_list_all",
        ]
        eventsubs = EventSub()
        test_pass = True

        for method in expected_methods:
            if not hasattr(eventsubs, method):
                logger.error("[UNITTEST] Failed finding %s", method)
                test_pass = False
        self.assertTrue(test_pass)

    def test_crud(self):
        """Ensure that we can add and remove subs and events"""

        def _outputter(_input):
            return _input

        eventsubs = EventSub()

        # Empty object, no subs / events
        self.assertIsInstance(eventsubs.sub_list(_outputter), tuple)
        self.assertIsInstance(eventsubs.event_list_all(), tuple)
        self.assertEqual(eventsubs.sub_list(_outputter), ())
        self.assertEqual(eventsubs.event_list_all(), ())

        # Create a sub, and an event by doing so
        self.assertTrue(eventsubs.sub_create(_outputter, "messages"))
        self.assertFalse(eventsubs.sub_create(_outputter, "messages"))
        self.assertEqual(eventsubs.sub_list(_outputter), ("messages",))
        self.assertEqual(eventsubs.event_list("messages"), (_outputter,))

        # Create an empty event
        self.assertTrue(eventsubs.event_create("testing"))
        self.assertFalse(eventsubs.event_create("testing"))
        self.assertEqual(
            eventsubs.event_list_all(),
            (
                "messages",
                "testing",
            ),
        )

        # Ensure callable is, in fact, callable
        self.assertEqual(eventsubs.event_list("messages")[0](1), 1)

        # Ensure we can unsub (event remains)
        self.assertFalse(eventsubs.sub_delete(_outputter, "not set"))
        self.assertTrue(eventsubs.sub_delete(_outputter, "messages"))
        self.assertFalse(eventsubs.sub_delete("Incorrect", "messages"))
        self.assertEqual(eventsubs.sub_list(_outputter), ())
        self.assertEqual(
            eventsubs.event_list_all(),
            (
                "messages",
                "testing",
            ),
        )

        # Create a few more subs
        for i in range(10):
            eventsubs.sub_create(_outputter, str(i))
            eventsubs.sub_create(self.test_crud, str(i))

        # Ensure unsub all works
        self.assertTrue(eventsubs.sub_wipe(_outputter))
        self.assertEqual(eventsubs.sub_list(_outputter), ())

        # Ensure we can destroy an event
        sublist = eventsubs.sub_list(self.test_crud)
        self.assertIn("5", sublist)
        self.assertTrue(eventsubs.event_delete("5"))
        sublist = eventsubs.sub_list(self.test_crud)
        self.assertNotIn("5", sublist)
