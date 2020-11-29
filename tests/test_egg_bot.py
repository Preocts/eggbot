import asyncio
import unittest
from unittest.mock import patch

from eggbot import eggbot_core as ec


def run_loop(func, *args, **kwargs):
    """ Hack to test async functions """
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(func(*args, **kwargs))
    return result


class TestEggbotCore(unittest.TestCase):
    def test_globals(self):
        self.assertIsInstance(ec.logger, ec.logging.Logger)
        self.assertIsInstance(ec.eggbot_config, ec.core_entities.CoreConfig)
        self.assertIsInstance(ec.discord_client, ec.discord.client.Client)
        self.assertIsInstance(ec.eventsub, ec.core_entities.EventSub)

    def test_config_load(self):
        self.assertTrue(ec.load_config())
        self.assertIsInstance(ec.eggbot_config, ec.core_entities.CoreConfig)
        self.assertIsNotNone(ec.eggbot_config.config)

    @patch("eggbot.eggbot_core.discord_client")
    def test_main(self, mock_client):
        # Load config
        # Configure Discord Client
        # (mock) Run discord bot
        # Deconstruct config
        # Clean exit
        ec.DISCORD_TOKEN = "Do not show secrets in test"
        ec.main()
        self.assertIsNone(ec.eggbot_config)
        mock_client.run.assert_called()
        mock_client.run.assert_called_with(ec.DISCORD_TOKEN)

    def test_join_event(self):
        with patch("eggbot.eggbot_core.discord_client") as mock:
            mock.user.id = "123456789"
            mock_member = unittest.mock.Mock()
            mock_member.id = "987654321"
            self.assertTrue(run_loop(ec.on_member_join, mock_member))

            mock_member.id = "123456789"
            self.assertFalse(run_loop(ec.on_member_join, mock_member))

    def test_message_event(self):
        with patch("eggbot.eggbot_core.discord_client") as mock:
            mock.user.id = "123456789"
            mock_message = unittest.mock.Mock()
            mock_message.author.id = "987654321"
            self.assertTrue(run_loop(ec.on_message, mock_message))

            mock_message.author.id = "123456789"
            self.assertFalse(run_loop(ec.on_message, mock_message))

