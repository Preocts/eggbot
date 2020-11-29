import unittest
from unittest.mock import patch

from eggbot import eggbot_core as ec


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

    async def test_join_event(self):
        mock_member = unittest.mock.Mock()
        await self.assertIsNone(ec.on_member_join(mock_member))

    async def test_message_event(self):
        mock_message = unittest.mock.Mock()
        await self.assertIsNone(ec.on_message(mock_message))
