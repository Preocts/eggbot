#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for ./modules/chatkudos.py

To run these tests from command line use the following:
    $ python -m pytest -v testes/test_module_chatkudos.py

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from unittest.mock import Mock

import pytest

from modules.chatkudos import ChatKudos
from modules.chatkudos import MODULE_NAME
from modules.chatkudos import MODULE_VERSION
from modules.chatkudos import COMMAND_CONFIG


@pytest.fixture(scope="function", name="kudos")
def fixture_kudos() -> ChatKudos:
    """ Fixture """
    return ChatKudos("./tests/fixtures/mock_chatkudos.json")


@pytest.fixture(scope="function", name="message")
def fixture_message() -> Mock:
    """ Fixture """
    message = Mock()
    message.content = "kudos!help"
    message.guild.name = "Testing Guild"
    message.guild.id = 111
    message.author.id = 111
    message.author.display_name = "Tester"
    return message


def test_does_fixture_need_updating(kudos: ChatKudos) -> None:
    """ Confirm version and module names match, sanity check """
    assert kudos.config.read("module") == MODULE_NAME
    assert kudos.config.read("version") == MODULE_VERSION


def test_command_config(kudos: ChatKudos) -> None:
    """ Ensure all commands have attr that exist """
    for attr in COMMAND_CONFIG.values():
        assert getattr(kudos, attr, None) is not None, f"Missing {attr} attribute"


def test_load_guild_found(kudos: ChatKudos) -> None:
    """ Load a guild that exists, check values """
    result = kudos.get_guild("111")
    assert result.max == -1
    assert result.users
    assert not result.roles


def test_load_guild_not_found(kudos: ChatKudos) -> None:
    """ Load a guild that doesn't exist, check defaults """
    result = kudos.get_guild("999")
    assert result.max == 5
    assert not result.users


def test_save_guild_exists(kudos: ChatKudos) -> None:
    """ Save explict changes, confirm existing don't change """
    kudos.save_guild("111", max=-1, gain_message="TEST")
    kudos.save_guild("111", loss_message="TEST02")

    assert kudos.get_guild("111").max == -1
    assert kudos.get_guild("111").gain_message == "TEST"
    assert kudos.get_guild("111").loss_message == "TEST02"


def test_save_guild_not_exists(kudos: ChatKudos) -> None:
    """ Save changes to a guild that does't exist """
    kudos.save_guild("999", max=-1, gain_message="TEST")
    kudos.save_guild("999", loss_message="TEST02")

    assert kudos.get_guild("999").max == -1
    assert kudos.get_guild("999").gain_message == "TEST"
    assert kudos.get_guild("999").loss_message == "TEST02"


def test_adjust_max(kudos: ChatKudos, message: Mock) -> None:
    """ Change max for existing and non-existing guild """
    message.content = "kudos!max 10"
    result = kudos.parse_command(message)
    assert "Max points set to 10" in result

    message.content = "kudos!max -1"
    message.guild.id = "999"
    result = kudos.parse_command(message)
    assert "Max points set to unlimited" in result

    assert kudos.get_guild("111").max == 10
    assert kudos.get_guild("999").max == -1


def test_adjust_max_invalid(kudos: ChatKudos, message: Mock) -> None:
    """ Provide an invalid format to the command """
    message.content = "kudos!max 10 points"
    result = kudos.parse_command(message)
    assert "Usage:" in result


def test_adjust_gain_messages(kudos: ChatKudos, message: Mock) -> None:
    """ Adjust the gain messages on existing and non-existing guilds """
    message.content = "kudos!gain This is gain"
    result = kudos.parse_command(message)
    assert "Message has been set." in result

    message.guild.id = "999"
    result = kudos.parse_command(message)
    assert "Message has been set." in result


def test_adjust_loss_messages(kudos: ChatKudos, message: Mock) -> None:
    """ Adjust the loss messages on existing and non-existing guilds """
    message.content = "kudos!loss This is loss"
    result = kudos.parse_command(message)
    assert "Message has been set." in result

    message.guild.id = "999"
    result = kudos.parse_command(message)
    assert "Message has been set." in result
