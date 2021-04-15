#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for ShoulderBird command line module

To run these tests from command line use the following:
    $ python -m pytest -v testes/test_module_shoulderbirdcli.py

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
from typing import NamedTuple
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from modules.shoulderbirdconfig import ShoulderBirdConfig
from modules.shoulderbirdcli import ShoulderbirdCLI


@pytest.fixture(scope="function", name="cli")
def fixture_cli() -> ShoulderbirdCLI:
    """ Create instance of CLI class"""
    config = ShoulderBirdConfig("./tests/fixtures/mock_shoulderbird.json")
    return ShoulderbirdCLI(config)


@pytest.fixture(scope="function", name="message")
def fixture_message() -> Mock:
    """ Returns a mock object for discord.message """
    return Mock()


class Guild(NamedTuple):
    """ Guild values """

    id: int
    name: str


def test_no_command_found(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Should fall-through """
    message.clean_content = "sb!boop"
    assert cli.parse_command(message) is None


def test_set_valid_guild_name(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Set a search by guild name """
    guilds = [Guild(10, "test"), Guild(9876543210, "testings")]
    message.clean_content = "sb!set testings = (search|find)"
    message.author.id = 111
    with patch.object(cli, "discord") as mock_discord:
        mock_discord.guilds = guilds
        result = cli.parse_command(message)
    assert result
    assert "Search set" in result

    member = cli.config.load_member("9876543210", "111")
    assert member is not None
    assert member.regex == "(search|find)"


def test_set_invalid_formatting(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Confirm failures based on return messages """
    message.clean_content = "sb!set myGuild But forgot the equal sign"
    result = cli.parse_command(message)
    assert result
    assert "Error: Formatting" in result

    message.clean_content = "sb!set myGuild = "
    result = cli.parse_command(message)
    assert result
    assert "Error: Formatting" in result


def test_set_invalid_guild(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Unknown guild/not in guild """
    guilds = [Guild(10, "test"), Guild(11, "testings")]
    message.clean_content = "sb!set myGuild = test"
    with patch.object(cli, "discord") as mock_discord:
        mock_discord.guilds = guilds
        result = cli.parse_command(message)

    assert result
    assert "Error: Guild not found" in result
