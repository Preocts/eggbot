"""
Unit tests for ./eggbot/exts/memberjoins.py

Author  : Preocts
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/eggbot
"""
from typing import Generator
from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from eggbot.exts.memberjoins import MemberJoins

TEST_CONFIG = "./tests/fixtures/memberjoins.toml"


@pytest.fixture(scope="function", name="member")
def fixture_member() -> Mock:
    """Fixture"""
    member = Mock()
    member.guild.id = 111
    member.guild.name = "Test Guild"
    member.name = "Tester01"
    member.mention = "@Tester01"
    member.bot = False
    return member


@pytest.fixture(scope="function", name="cog")
def fixture_cog() -> Generator[MemberJoins, None, None]:
    """Fixture"""
    with patch.object(MemberJoins, "DEFAULT_CONFIG", TEST_CONFIG):
        yield MemberJoins()


def test_read_actions_guild_not_found(cog: MemberJoins) -> None:
    """Attempt to get actions for a guild not in config"""
    result = cog.get_actions("999")
    assert not result


def test_read_actions_guild_found(cog: MemberJoins) -> None:
    """Attempt to get actions for a guild, ensure expected exist"""
    expected_names = ["test01", "test02", "test03"]
    result = cog.get_actions("111")
    assert len(result) == 3
    for action in result:
        assert action.name in expected_names, action


def test_message_formatter(cog: MemberJoins, member: Mock) -> None:
    """Ensure we create metavalues correctly"""

    msg = "-[USERNAME]- has joined [GUILDNAME]"
    assert cog.format_content(msg, member) == "-Tester01- has joined Test Guild"


def test_all_metadata(cog: MemberJoins, member: Mock) -> None:
    """Step through all metadata config, ensure everything works"""
    for key in cog.METADATA:
        assert cog.format_content(key, member)


@pytest.mark.asyncio
async def test_on_join_with_actions_success(cog: MemberJoins, member: Mock) -> None:
    """On Join event with two actions (channel and DM)"""

    send_dm = AsyncMock()
    send_channel = AsyncMock()
    with patch.multiple(cog, _send_dm=send_dm, _send_channel=send_channel):
        await cog.on_member_join(member)
        send_channel.assert_called_once()
        send_dm.assert_called_once()


@pytest.mark.asyncio
async def test_on_join_with_no_actions(cog: MemberJoins, member: Mock) -> None:
    """On Join event with no actions"""
    member.guild.id = 999

    send_dm = AsyncMock()
    send_channel = AsyncMock()
    with patch.multiple(cog, _send_dm=send_dm, _send_channel=send_channel):
        await cog.on_member_join(member)
        send_channel.assert_not_called()
        send_dm.assert_not_called()


@pytest.mark.asyncio
async def test_on_join_of_bot(cog: MemberJoins, member: Mock) -> None:
    """On Join event of a bot"""
    member.guild.id = 111
    member.bot = True

    send_dm = AsyncMock()
    send_channel = AsyncMock()
    with patch.multiple(cog, _send_dm=send_dm, _send_channel=send_channel):
        await cog.on_member_join(member)
        send_channel.assert_not_called()
        send_dm.assert_not_called()


@pytest.mark.asyncio
async def test_send_channel(cog: MemberJoins) -> None:
    """Send a message to a channel"""
    guild = Mock()
    channel = AsyncMock()
    guild.get_channel = Mock(return_value=channel)

    await cog._send_channel("test", "1", guild)

    assert channel.send.call_count == 1


@pytest.mark.asyncio
async def test_send_channel_fail(cog: MemberJoins) -> None:
    """Send a message to a channel"""
    guild = Mock()
    guild.get_channel = Mock(return_value=None)

    await cog._send_channel("test", "1", guild)


@pytest.mark.asyncio
async def test_send_dm_success(cog: MemberJoins) -> None:
    member = Mock()
    member.dm_channel = AsyncMock()
    member.dm_channel.send = AsyncMock()

    await cog._send_dm("test", member)

    assert member.dm_channel.send.call_count == 1


@pytest.mark.asyncio
async def test_send_dm_fail(cog: MemberJoins) -> None:
    member = Mock()
    member.dm_channel = False
    member.create_dm = AsyncMock()

    await cog._send_dm("test", member)

    assert member.create_dm.call_count == 1
