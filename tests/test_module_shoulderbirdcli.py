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

from modules.shoulderbirdcli import COMMAND_CONFIG
from modules.shoulderbirdcli import ShoulderbirdCLI
from modules.shoulderbirdconfig import ShoulderBirdConfig


@pytest.fixture(scope="function", name="cli")
def fixture_cli() -> ShoulderbirdCLI:
    """ Create instance of CLI class"""
    config = ShoulderBirdConfig("./tests/fixtures/mock_shoulderbirdcli.json")
    return ShoulderbirdCLI(config)


@pytest.fixture(scope="function", name="message")
def fixture_message() -> Mock:
    """ Returns a mock object for discord.message """
    return Mock()


class Guild(NamedTuple):
    """ Mocked Guild object """

    id: int
    name: str


class User(NamedTuple):
    """ Mocked User object """

    id: int
    name: str


def test_no_command_found(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Should fall-through """
    message.clean_content = "sb!boop"
    assert cli.parse_command(message) is None


def test_set_valid_guild_name_new(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Set a search by guild name that doesn't exist """
    guilds = [Guild(10, "test"), Guild(9876543210, "testings")]
    message.clean_content = "sb!set testings = (search|find)"
    message.author.id = 111
    with patch.object(cli, "discord") as mock_discord:
        mock_discord.guilds = guilds
        result = cli.parse_command(message)
    assert result
    assert "Search set" in result

    member = cli.config.load_member("9876543210", "111")
    assert member.regex == "(search|find)"


def test_set_valid_id_exists(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Set a search by guild ID that does exist """
    guilds = [Guild(101, "test"), Guild(9876543210, "testings")]
    message.clean_content = "sb!set 101 = (search|find)"
    message.author.id = 101
    with patch.object(cli, "discord") as mock_discord:
        mock_discord.guilds = guilds
        result = cli.parse_command(message)
    assert result
    assert "Search set" in result

    member = cli.config.load_member("101", "101")
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


def test_toggle_on_guild_found(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Guild found in config, turn toggle on """
    message.clean_content = "sb!on"
    message.author.id = 101
    result = cli.parse_command(message)

    assert result
    assert "ShoulderBird now **on**" in result


def test_toggle_on_guild_not_found(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Guild not found in config, nothing to turn on """
    message.clean_content = "sb!on"
    message.author.id = 901
    result = cli.parse_command(message)

    assert result
    assert "No searches found," in result


def test_toggle_off_guild_found(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Guild found in config, turn toggle off """
    message.clean_content = "sb!off"
    message.author.id = 101
    result = cli.parse_command(message)

    assert result
    assert "ShoulderBird now **off**" in result


def test_toggle_off_guild_not_found(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Guild not found in config, nothing to turn off """
    message.clean_content = "sb!off"
    message.author.id = 901
    result = cli.parse_command(message)

    assert result
    assert "No searches found," in result


def test_ignore_no_target(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Ignore command but nothing given """
    message.clean_content = "sb!ignore "
    result = cli.parse_command(message)

    assert result
    assert "Error: Formatting" in result


def test_ignore_user_not_found(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Username not found, return helpful tips """
    message.clean_content = "sb!ignore dave"
    users = [User(10, "test"), User(9876543210, "test_user")]
    with patch.object(cli, "discord") as mock_discord:
        mock_discord.users = users
        result = cli.parse_command(message)

        assert result
        assert "'dave' not found." in result


def test_ignore_name_toggle_target(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Ignore a user, confirm. Unignore user, confirm """
    message.clean_content = "sb!ignore test_user"
    message.author.id = 901
    users = [User(10, "test"), User(9876543210, "test_user")]
    with patch.object(cli, "discord") as mock_discord:
        mock_discord.users = users
        ignored_result = cli.parse_command(message)

        assert ignored_result
        assert "'test_user' added to" in ignored_result

        for member in cli.config.member_list_all("901"):
            assert "9876543210" in member.ignore, member.guild_id

        message.clean_content = "sb!unignore test_user"
        unignored_result = cli.parse_command(message)

        assert unignored_result
        assert "'test_user' removed from" in unignored_result

        for member in cli.config.member_list_all("901"):
            assert "9876543210" not in member.ignore, member.guild_id


def test_help(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Check for good help responses """
    message.clean_content = "sb!help"
    result = cli.parse_command(message)

    assert result
    assert COMMAND_CONFIG["sb!help"]["help"] in result


def test_all_helps(cli: ShoulderbirdCLI, message: Mock) -> None:
    """ Checks all helps in COMMAND_CONFIG """
    for key, values in COMMAND_CONFIG.items():
        message.clean_content = f"sb!help {key.replace('sb!', '')}"
        result = cli.parse_command(message)

        assert result
        assert values["help"] in result, key


def test_sanitize_search(cli: ShoulderbirdCLI) -> None:
    """ Regex injection is a thing apparently """
    safe_re = "(simple|Complex)"
    assert cli.sanitize_search(safe_re) == "(simple|complex)"

    questionable = "(Simple|c*ompl+ex?|a{5})\\"
    assert cli.sanitize_search(questionable) == r"(simple|c\*ompl\+ex\?|a\{5\})\\"
