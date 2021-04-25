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
import pytest

from modules.module_shoulderbirdparser import ShoulderBirdParser


@pytest.fixture(scope="function", name="parser")
def fixture_parser() -> ShoulderBirdParser:
    """ fixture """
    return ShoulderBirdParser("./tests/fixtures/mock_shoulderbirdparser.json")


def test_positive_match_simple(parser: ShoulderBirdParser) -> None:
    """ Positive matches, also tests toggle """
    matches = parser.get_matches("101", "Delta", "This is a test")
    assert len(matches) == 2
    for idx, match in enumerate(matches):
        assert match.member_id == f"10{idx + 1}"


def test_positive_match_complex(parser: ShoulderBirdParser):
    """ Positive match, tests for case agnostic """
    msg = "I should hope this TESTsuite passes!"
    matches = parser.get_matches("102", "Delta", msg)
    assert len(matches) == 1
    assert matches[0].member_id == "101"


def test_word_bound_regex_complex_search(parser: ShoulderBirdParser):
    """ Negitive match, ensure word bound is applied """
    msg = "appreciated"
    matches = parser.get_matches("101", "Delta", msg)
    assert len(matches) == 0
    msg = "preoct"
    matches = parser.get_matches("101", "Delta", msg)
    assert len(matches) == 1
