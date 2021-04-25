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
from unittest.mock import Mock
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest

from modules.module_joinactions import JoinActions
from modules.module_joinactions import MODULE_NAME
from modules.module_joinactions import MODULE_VERSION
from modules.module_joinactions import METADATA


@pytest.fixture(scope="function", name="member")
def fixture_member() -> Mock:
    """ Fixture """
    member = Mock()
    member.guild.id = 111
    member.guild.name = "Test Guild"
    member.name = "Tester01"
    member.mention = "@Tester01"
    member.bot = False
    return member


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


def test_message_formatter(join: JoinActions, member: Mock) -> None:
    """ Ensure we create metavalues correctly """

    msg = "-[USERNAME]- has joined [GUILDNAME]"
    assert join.format_content(msg, member) == "-Tester01- has joined Test Guild"


def test_all_metadata(join: JoinActions, member: Mock) -> None:
    """ Step through all metadata config, ensure everything works """
    for key in METADATA:
        assert join.format_content(key, member)


@pytest.mark.asyncio
async def test_on_join_with_actions_success(join: JoinActions, member: Mock) -> None:
    """ On Join event with two actions (channel and DM) """

    send_dm = AsyncMock()
    send_channel = AsyncMock()
    with patch.multiple(join, _send_dm=send_dm, _send_channel=send_channel):
        await join.on_member_join(member)
        send_channel.assert_called_once()
        send_dm.assert_called_once()


@pytest.mark.asyncio
async def test_on_join_with_no_actions(join: JoinActions, member: Mock) -> None:
    """ On Join event with no actions """
    member.guild.id = 999

    send_dm = AsyncMock()
    send_channel = AsyncMock()
    with patch.multiple(join, _send_dm=send_dm, _send_channel=send_channel):
        await join.on_member_join(member)
        send_channel.assert_not_called()
        send_dm.assert_not_called()
