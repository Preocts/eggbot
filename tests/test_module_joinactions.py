#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for ./modules/joinactions.py

To run these tests from command line use the following:
    $ python -m pytest -v testes/test_module_shoulderbirdcli.py

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import pytest

from modules.joinactions import JoinActions
from modules.joinactions import MODULE_NAME
from modules.joinactions import MODULE_VERSION


@pytest.fixture(scope="function", name="join")
def fixture_join() -> JoinActions:
    """ Fixture """
    return JoinActions("./tests/fixtures/mock_joinactions.json")


def test_does_fixture_need_updating(join: JoinActions) -> None:
    """ Confirm version and module names match, sanity check """
    assert join.config.read("module") == MODULE_NAME
    assert join.config.read("version") == MODULE_VERSION


def test_read_actions_guild_not_found(join: JoinActions) -> None:
    """ Attempt to get actions for a guild not in config """
    result = join.get_actions("999")
    assert not result


def test_read_actions_guild_found(join: JoinActions) -> None:
    """ Attempt to get actions for a guild, ensure expected exist """
    expected_names = ["test01", "test02", "test03"]
    result = join.get_actions("111")
    assert len(result) == 3
    for action in result:
        assert action.name in expected_names, action
