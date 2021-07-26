#!/usr/bin/env python3
"""
Unit tests for ShoulderBird config module

To run these tests from command line use the following:
    $ python -m pytest -v testes/test_module_shoulderbirdconfig.py

These tests create and destroy their own mock config file within
`./tests/fixtures` for validation.

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
from typing import Optional

from modules.shoulderbirdconfig import ShoulderBirdConfig

MOCK_CONFIG = "tests/fixtures/mock_shoulderbird.json"
MOCK_GUILD_ID = "9876543210"
MOCK_MEMBER_ID = "0123456789"


class TestShoulderBirdConfig:
    """Test suite"""

    parser: Optional[ShoulderBirdConfig] = None

    def test_empty_config(self) -> None:
        """Start with non-existing config"""
        if os.path.isfile(MOCK_CONFIG):
            os.remove(MOCK_CONFIG)
        assert not os.path.isfile(MOCK_CONFIG)
        TestShoulderBirdConfig.parser = ShoulderBirdConfig(MOCK_CONFIG)
        assert self.parser is not None
        assert self.parser.save_config()
        assert os.path.isfile(MOCK_CONFIG)

    def test_save_new_and_load(self) -> None:
        """Ensure we save a new member and recall info after unload"""
        assert self.parser is not None
        self.parser.save_member(MOCK_GUILD_ID, MOCK_MEMBER_ID, toggle=False)
        assert self.parser.save_config()
        assert self.parser.reload_config()
        self.parser = ShoulderBirdConfig(MOCK_CONFIG)
        member = self.parser.load_member(MOCK_GUILD_ID, MOCK_MEMBER_ID)
        assert not member.toggle

    def test_reload_without_save(self) -> None:
        """Forced reload should loose all changes"""
        assert self.parser is not None
        before_reload = self.parser.load_member(MOCK_GUILD_ID, MOCK_MEMBER_ID)
        self.parser.save_member(
            MOCK_GUILD_ID, MOCK_MEMBER_ID, regex="boom", toggle=True
        )
        assert self.parser.reload_config()
        after_reload = self.parser.load_member(MOCK_GUILD_ID, MOCK_MEMBER_ID)
        assert before_reload.regex == after_reload.regex
        assert before_reload.toggle is after_reload.toggle

    def test_modify_existing(self) -> None:
        """Ensure we modify a save while preserving existing values"""
        assert self.parser is not None
        prior_member = self.parser.load_member(MOCK_GUILD_ID, MOCK_MEMBER_ID)
        self.parser.save_member(MOCK_GUILD_ID, MOCK_MEMBER_ID, regex="test")
        modded_member = self.parser.load_member(MOCK_GUILD_ID, MOCK_MEMBER_ID)
        assert prior_member.regex == ""
        assert modded_member.regex == "test"
        assert not modded_member.toggle
        assert self.parser.save_config()

    def test_delete_member(self) -> None:
        """Ensure we delete correctly"""
        assert self.parser is not None
        assert self.parser.delete_member(MOCK_GUILD_ID, MOCK_MEMBER_ID)
        assert not self.parser.delete_member(MOCK_GUILD_ID, MOCK_MEMBER_ID)
        assert self.parser.save_config()

    def test_mutli_guilds(self) -> None:
        """Can we get all the guilds of a single member"""
        assert self.parser is not None
        guild_ids = ["123", "1234", "12345", "123456"]
        for ids in guild_ids:
            self.parser.save_member(ids, MOCK_MEMBER_ID, regex="multi-test")
        configs = self.parser.member_list_all(MOCK_MEMBER_ID)
        assert len(configs) == 4
        for config in configs:
            assert config.regex == "multi-test"
        self.parser.reload_config()

    def test_multi_members(self) -> None:
        """Create and read multi-members in one guild"""
        assert self.parser is not None
        member_ids = ["123", "1234", "12345", "123456"]
        for ids in member_ids:
            self.parser.save_member(MOCK_GUILD_ID, ids, regex="multi-test")
        configs = self.parser.guild_list_all(MOCK_GUILD_ID)
        assert len(configs) == 4
        for config in configs:
            assert config.regex == "multi-test"
        self.parser.reload_config()
