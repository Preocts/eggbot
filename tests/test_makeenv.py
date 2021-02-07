#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- condig: utf-8 -*-
""" Unit tests for makeenv.py

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
import unittest

from eggbot.utils.loadenv import LoadEnv


class TestLoadEnv(unittest.TestCase):
    """ Test suite """

    def test_loads_mock_target(self):
        """ Load test """
        env = LoadEnv("./tests/fixtures")
        self.assertEqual(env.get("test"), "success")
        self.assertEqual(env.get("test2"), "even more success")
        self.assertEqual(env.get("test3"), "")
        self.assertEqual(env.get("test4"), "Final test")

    def test_unload_mock_target(self):
        """ Unload test """
        env = LoadEnv("./tests/fixtures")
        self.assertIsNotNone(os.environ.get("test"), None)
        del env
        self.assertIsNone(os.environ.get("test"), None)
