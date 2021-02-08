# -*- coding: utf-8 -*-
""" Unit Tests

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
import shutil
import unittest

from eggbot.eventsub import EventSub


class TestEventSub(unittest.TestCase):
    """ Test Suite """

    def test_load_modules(self):
        """ Pass/Fail loading modules """
        event_client = EventSub()
        shutil.move("./modules", "./modules_test")
        try:
            self.assertFalse(event_client.load_modules())
        finally:
            shutil.move("./modules_test", "./modules")
        shutil.copy("./tests/fixtures/mock_module.py", "./modules/module_mock.py")
        try:
            with self.assertRaises(Exception):
                event_client.load_modules()
        finally:
            os.remove("./modules/module_mock.py")
