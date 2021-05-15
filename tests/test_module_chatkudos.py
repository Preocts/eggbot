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
from collections import namedtuple
from typing import Generator
from typing import List
from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from modules.module_chatkudos import ChatKudos
from modules.module_chatkudos import COMMAND_CONFIG
from modules.module_chatkudos import Kudos
from modules.module_chatkudos import MODULE_NAME
from modules.module_chatkudos import MODULE_VERSION


@pytest.fixture(scope="function", name="kudos")
def fixture_kudos() -> Generator[ChatKudos, None, None]:
    """Fixture"""
    kudos = ChatKudos("./tests/fixtures/mock_chatkudos.json")
    # disable writing to the fixture file
    with patch.object(kudos.config, "save"):
        yield kudos


@pytest.fixture(scope="function", name="message")
def fixture_message() -> Mock:
    """Fixture"""
    members: List[Mock] = [
        Mock(display_name="Tester01"),
        Mock(display_name="Tester02"),
    ]

    mentions = Mock(id=111, display_name="Tester")

    role_mentions = Mock(id=987)
    role_mentions.name = "Cool Kats"

    message = Mock()
    message.content = "kudos!help"
    message.guild.name = "Testing Guild"
    message.guild.id = 111
    message.guild.owner.id = 333
    message.author.id = 111
    message.author.display_name = "Tester"
    message.channel.type = "text"
    message.mentions = [mentions]
    message.role_mentions = [role_mentions]
    message.guild.get_member.side_effect = members
    return message


@pytest.fixture(scope="function", name="async_message")
def fixture_async_message() -> AsyncMock:
    """Fixture"""
    message = AsyncMock()
    message.content = "<#!111> + <!222#> + Oh yeah baby!"
    message.guild.name = "Testing Guild"
    message.guild.id = 111
    message.guild.owner.id = 333
    message.author.id = 222
    message.author.display_name = "Tester"
    message.channel.type = "text"
    message.mentions = [
        AsyncMock(id="111", display_name="Tester01"),
        AsyncMock(id="222", display_name="Tester02"),
    ]

    return message


def test_does_fixture_need_updating(kudos: ChatKudos) -> None:
    """Confirm version and module names match, sanity check"""
    assert kudos.config.read("module") == MODULE_NAME
    assert kudos.config.read("version") == MODULE_VERSION


def test_command_config(kudos: ChatKudos) -> None:
    """Ensure all commands have attr that exist"""
    for attr in COMMAND_CONFIG.values():
        assert getattr(kudos, attr, None) is not None, f"Missing {attr} attribute"


def test_load_guild_found(kudos: ChatKudos) -> None:
    """Load a guild that exists, check values"""
    result = kudos.get_guild("111")
    assert result.max == -1
    assert result.users
    assert not result.roles


def test_load_guild_not_found(kudos: ChatKudos) -> None:
    """Load a guild that doesn't exist, check defaults"""
    result = kudos.get_guild("999")
    assert result.max == 5
    assert not result.users


def test_save_guild_exists(kudos: ChatKudos) -> None:
    """Save explict changes, confirm existing don't change"""
    kudos.save_guild("111", max=-1, gain_message="TEST")
    kudos.save_guild("111", loss_message="TEST02")

    assert kudos.get_guild("111").max == -1
    assert kudos.get_guild("111").gain_message == "TEST"
    assert kudos.get_guild("111").loss_message == "TEST02"


def test_save_guild_not_exists(kudos: ChatKudos) -> None:
    """Save changes to a guild that does't exist"""
    kudos.save_guild("999", max=-1, gain_message="TEST")
    kudos.save_guild("999", loss_message="TEST02")

    assert kudos.get_guild("999").max == -1
    assert kudos.get_guild("999").gain_message == "TEST"
    assert kudos.get_guild("999").loss_message == "TEST02"


def test_adjust_max(kudos: ChatKudos, message: Mock) -> None:
    """Change max for existing and non-existing guild"""
    message.content = "kudos!max 10"
    result = kudos.parse_command(message)
    assert "Max points now: 10" in result

    message.content = "kudos!max -1"
    message.guild.id = "999"
    result = kudos.parse_command(message)
    assert "Max points now: unlimited" in result

    assert kudos.get_guild("111").max == 10
    assert kudos.get_guild("999").max == -1


def test_adjust_max_invalid(kudos: ChatKudos, message: Mock) -> None:
    """Provide an invalid format to the command"""
    message.content = "kudos!max 10 points"
    result = kudos.parse_command(message)
    assert "Usage:" in result


def test_adjust_gain_messages(kudos: ChatKudos, message: Mock) -> None:
    """Adjust the gain messages on existing and non-existing guilds"""
    message.content = "kudos!gain This is gain"
    result = kudos.parse_command(message)
    assert "Message has been set." in result
    assert kudos.get_guild("111").gain_message == "This is gain"

    message.guild.id = "999"
    result = kudos.parse_command(message)
    assert "Message has been set." in result
    assert kudos.get_guild("999").gain_message == "This is gain"


def test_adjust_loss_messages(kudos: ChatKudos, message: Mock) -> None:
    """Adjust the loss messages on existing and non-existing guilds"""
    message.content = "kudos!loss This is loss"
    result = kudos.parse_command(message)
    assert "Message has been set." in result
    assert kudos.get_guild("111").loss_message == "This is loss"

    message.guild.id = "999"
    result = kudos.parse_command(message)
    assert "Message has been set." in result
    assert kudos.get_guild("999").loss_message == "This is loss"


def test_adjust_message_empty(kudos: ChatKudos, message: Mock) -> None:
    """Confirm an empty message is skipped"""
    message.content = "kudos!gain"
    result = kudos.parse_command(message)
    assert not result


def test_add_remove_user_list(kudos: ChatKudos, message: Mock) -> None:
    """Add, then remove, a user from user list"""
    message.role_mentions = []  # Clear to focus test scope
    message.content = "kudos!user @Tester"  # mention is provided by fixture

    result = kudos.parse_command(message)
    assert "**+**Tester" in result
    assert "111" in kudos.get_guild("111").users

    result = kudos.parse_command(message)
    assert "**-**Tester" in result
    assert "111" not in kudos.get_guild("111").users


def test_add_remove_role_list(kudos: ChatKudos, message: Mock) -> None:
    """Add, then remove, a role from role list"""
    message.mentions = []  # Clear to focus test scope
    message.content = "kudos!role @Cool Kats"  # role_mention provided by fixture

    result = kudos.parse_command(message)
    assert "**+**Cool Kats" in result
    assert "987" in kudos.get_guild("111").roles

    result = kudos.parse_command(message)
    assert "**-**Cool Kats" in result
    assert "987" not in kudos.get_guild("111").roles


def test_add_remove_list_empty(kudos: ChatKudos, message: Mock) -> None:
    """Confirm message with no mentions is skipped"""
    message.role_mentions = []
    message.mentions = []
    message.content = "kudos!user This is just an empty message"

    result = kudos.parse_command(message)
    assert not result


def test_lock_toggle(kudos: ChatKudos, message: Mock) -> None:
    """Turn the lock on and off again, fixture starts locked"""
    message.content = "kudos!lock"

    result = kudos.parse_command(message)
    assert result == "ChatKudos is now unlocked. **Everyone** can use it!"
    assert not kudos.get_guild("111").lock

    result = kudos.parse_command(message)
    assert result == "ChatKudos is now locked. Only allowed users/roles can use it!"
    assert kudos.get_guild("111").lock


def test_help(kudos: ChatKudos, message: Mock) -> None:
    """Does this have a help?"""
    message.content = "kudos!help"

    result = kudos.parse_command(message)
    assert "https://github.com/Preocts/eggbot/blob/main/docs/chatkudos.md" in result


def test_board_all(kudos: ChatKudos, message: Mock) -> None:
    """Print the board without # limit"""
    message.content = "kudos!board Give me all the board"

    result = kudos.parse_command(message)
    assert "Top 10 ChatKudos holders:" in result
    assert "Tester01" in result
    assert "Tester02" in result


def test_board_limited(kudos: ChatKudos, message: Mock) -> None:
    """Print the board with a # limit"""
    message.content = "kudos!board 1"

    result = kudos.parse_command(message)
    assert "Top 1 ChatKudos holders:" in result
    assert "Tester01" in result
    assert "Tester02" not in result


def test_find_kudos(kudos: ChatKudos, message: Mock) -> None:
    """Return the accurate Kudos count for messages"""
    message.content = "<#!111> ++-++-++ <!222#> just kidding"
    message.mentions = [
        Mock(id="111", display_name="Tester01"),
        Mock(id="222", display_name="Tester02"),
    ]

    result = kudos.find_kudos(message)
    assert len(result) == 1
    assert result[0].display_name == "Tester01"
    assert result[0].amount == 4
    assert result[0].current == -38

    kudos.save_guild("111", max=1)
    result = kudos.find_kudos(message)
    assert result[0].amount == 1


def test_format_message() -> None:
    """Message formatting"""
    msg = "Fantastic [NAME], have [POINTS] Kudos points. You now have [TOTAL] in total."
    expect = "Fantastic Tester01, have 15 Kudos points. You now have 30 in total."
    kudos = Kudos("111", "Tester01", 15, 15)

    result = ChatKudos._format_message(msg, kudos)  # pylint: disable=W0212

    assert result == expect


@pytest.mark.asyncio
async def test_onmessage_kudos(kudos: ChatKudos, async_message: AsyncMock) -> None:
    """Give two Kudos. Config should update"""
    await kudos.on_message(async_message)

    scores = kudos.get_guild("111").scores
    assert scores["111"] == -37
    assert scores["222"] == 1

    async_message.channel.send.assert_called()
    assert async_message.channel.send.call_count == 2


@pytest.mark.asyncio
async def test_onmessage_command(kudos: ChatKudos, async_message: AsyncMock) -> None:
    """Give a command, ensure we hit the command path"""
    async_message.content = "kudos!help"

    await kudos.on_message(async_message)

    async_message.channel.send.assert_called_once()


def test_is_command_allowed(kudos: ChatKudos, message: Mock) -> None:
    """Case checks for accessing commands"""
    kudos.save_guild("111", lock=True)
    # Server Owner
    message.content = "kudos!help"
    message.author.id = "333"
    assert kudos.is_command_allowed(message)

    # On User List
    message.author.id = "111"
    kudos.save_guild("111", users=["111"])
    assert kudos.is_command_allowed(message)

    # Not on User List
    message.author.id = "999"
    assert not kudos.is_command_allowed(message)


def test_is_kudos_allowed(kudos: ChatKudos, message: Mock) -> None:
    """Case checks for accessing Kudos, only new test is role list"""

    # On Role List
    Roles = namedtuple("Roles", ["id"])
    message.author.roles = [Roles(112), Roles(113), Roles(114)]
    message.content = "@Tester1 +++"
    kudos.save_guild("111", users=[], roles=["114"])
    assert kudos.is_kudos_allowed(message)

    # Not allowed on lock
    kudos.save_guild("111", roles=[])
    assert not kudos.is_kudos_allowed(message)

    # Unlock and pass
    kudos.save_guild("111", lock=False)
    assert kudos.is_kudos_allowed(message)
