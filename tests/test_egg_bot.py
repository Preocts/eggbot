import unittest
from unittest.mock import patch

from eggbot import eggbot_core


class TestEggbotCore(unittest.TestCase):

    def test_globals(self):
        self.assertIsInstance(
            eggbot_core.logger,
            eggbot_core.logging.Logger
        )
        self.assertIsInstance(
            eggbot_core.eggbot_config,
            eggbot_core.core_entities.CoreConfig
        )

        self.assertIsInstance(
            eggbot_core.discord_client,
            eggbot_core.discord.client.Client
        )

    def test_config_load(self):
        self.assertTrue(eggbot_core.load_config())
        self.assertIsInstance(
            eggbot_core.eggbot_config,
            eggbot_core.core_entities.CoreConfig
        )
        self.assertIsNotNone(eggbot_core.eggbot_config.config)

    @patch('eggbot.eggbot_core.discord_client')
    def test_main(self, mock_client):
        # Load config
        # Configure Discord Client
        # (mock) Run discord bot
        # Deconstruct config
        # Clean exit
        eggbot_core.DISCORD_TOKEN = 'Do not show secrets in test'
        eggbot_core.main()
        self.assertIsNone(eggbot_core.eggbot_config)
        mock_client.run.assert_called()
        mock_client.run.assert_called_with(eggbot_core.DISCORD_TOKEN)
