#!/usr/bin/env python3
""" Testing suite """
import unittest
from unittest.mock import patch

from eggbot.discordclient import DiscordClient


class TestDiscordClient(unittest.TestCase):
    """Discord Client Abstract"""

    def test_singleton_assignment(self):
        """One client and only one client"""
        client1 = DiscordClient()
        client2 = DiscordClient()
        self.assertIs(client1, client2)

    def test_assert_run_with_secret(self):
        """Use all the things"""
        client = DiscordClient()
        client.set_secret("Hello there")
        with patch.object(client.client, "run") as mock_discord:
            client.run()
            mock_discord.assert_called_once_with("Hello there")
