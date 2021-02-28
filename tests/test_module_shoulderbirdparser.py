#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for ShoulderBird parser module

To run these tests from command line use the following:
    $ python -m pytest -v testes/test_module_shoulderbirdparser.py

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""

from modules.shoulderbirdparser import ShoulderBirdParser


class TestShoulderBirdParser:
    """ Test suite """

    # pylint: disable=attribute-defined-outside-init
    def setup_method(self):
        """ Fixture Creation """
        self.parser = ShoulderBirdParser(
            "./tests/fixtures/mock_shoulderbirdparser.json"
        )
        self.mock_call = {
            "guild_id": "01",
            "user_id": "Delta",
            "clean_message": "I should hope this test passes!",
        }

    def test_positive_match_simple(self):
        """ Positive match, also tests toggle """
        matches = self.parser.get_matches(**self.mock_call)
        assert len(matches) == 2
        for idx, match in enumerate(matches):
            assert match.member_id == f"0{idx + 1}"

    def test_positive_match_complex(self):
        """ Positive match, tests for case agnostic """
        self.mock_call["clean_message"] = "I should hope this TESTsuite passes!"
        matches = self.parser.get_matches(**self.mock_call)
        assert len(matches) == 1
        assert matches[0].member_id == "01"

    def test_word_bound_regex(self):
        """ Negitive match, ensure word bound is applied """
        self.mock_call["clean_message"] = "Ishouldhopethistestpasses!"
        matches = self.parser.get_matches(**self.mock_call)
        assert len(matches) == 0
