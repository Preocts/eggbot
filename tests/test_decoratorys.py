# -*- coding: utf-8 -*-
""" Ensure decorators return the expected results from decorated func """
import unittest

from eggbot.utils import logdec


class TestLogDecorators(unittest.TestCase):
    def test_debug(self):
        @logdec.debug_log
        def sample_out(value: str) -> str:
            return value

        self.assertEqual(sample_out("Hello"), "Hello")
