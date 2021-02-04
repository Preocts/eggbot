""" Egg Bot, Discord Modular Bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
import unittest


from eggbot import core_entities as ce


logger = logging.getLogger(__name__)


class TestEventSub(unittest.TestCase):
    """ Runs tests against the object of EventSub and children """

    def test_object_methods(self):
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
        eventSubs = ce.EventSub()
        test_pass = True

        for method in expected_methods:
            if not hasattr(eventSubs, method):
                logger.error(f"[UNITTEST] Failed finding {method}")
                test_pass = False
        self.assertTrue(test_pass)

    def test_crud(self):
        """Ensure that we can add and remove subs and events"""

        def _outputter(_input):
            return _input

        spub = ce.EventSub()

        # Empty object, no subs / events
        self.assertIsInstance(spub.sub_list(_outputter), tuple)
        self.assertIsInstance(spub.event_list_all(), tuple)
        self.assertEqual(spub.sub_list(_outputter), ())
        self.assertEqual(spub.event_list_all(), ())

        # Create a sub, and an event by doing so
        self.assertTrue(spub.sub_create(_outputter, "messages"))
        self.assertFalse(spub.sub_create(_outputter, "messages"))
        self.assertEqual(spub.sub_list(_outputter), ("messages",))
        self.assertEqual(spub.event_list("messages"), (_outputter,))

        # Create an empty event
        self.assertTrue(spub.event_create("testing"))
        self.assertFalse(spub.event_create("testing"))
        self.assertEqual(
            spub.event_list_all(),
            (
                "messages",
                "testing",
            ),
        )

        # Ensure callable is, in fact, callable
        self.assertEqual(spub.event_list("messages")[0](1), 1)

        # Ensure we can unsub (event remains)
        self.assertFalse(spub.sub_delete(_outputter, "not set"))
        self.assertTrue(spub.sub_delete(_outputter, "messages"))
        self.assertFalse(spub.sub_delete("Incorrect", "messages"))
        self.assertEqual(spub.sub_list(_outputter), ())
        self.assertEqual(
            spub.event_list_all(),
            (
                "messages",
                "testing",
            ),
        )

        # Create a few more subs
        for i in range(10):
            spub.sub_create(_outputter, str(i))
            spub.sub_create(self.test_crud, str(i))

        # Ensure unsub all works
        self.assertTrue(spub.sub_wipe(_outputter))
        self.assertEqual(spub.sub_list(_outputter), ())

        # Ensure we can destroy an event
        sublist = spub.sub_list(self.test_crud)
        self.assertIn("5", sublist)
        self.assertTrue(spub.event_delete("5"))
        sublist = spub.sub_list(self.test_crud)
        self.assertNotIn("5", sublist)
