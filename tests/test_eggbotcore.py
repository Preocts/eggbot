# -*- coding: utf-8 -*-
""" Testing suite """
import asyncio
import unittest
from unittest.mock import patch

from eggbot import eggbotcore as ec
from eggbot.configfile import ConfigFile


def run_loop(func, *args, **kwargs):
    """ Hack to test async functions """
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(func(*args, **kwargs))
    return result


class TestEggbotCore(unittest.TestCase):
    """ Testing suite """

    def test_globals(self):
        """ These need to exist """
        self.assertIsInstance(ec.logger, ec.logging.Logger)
        self.assertIsInstance(ec.discord_client, ec.discord.client.Client)
        self.assertIsInstance(ec.eventSubs, ec.EventSub)
        self.assertIsInstance(ec.coreConfig, ConfigFile)

    def test_config_load(self):
        """ Pass fail on config load """
        self.assertTrue(ec.load_config())
        with patch.object(ec.coreConfig, "load", return_value=False):
            self.assertFalse(ec.load_config())

    @patch("eggbot.eggbotcore.discord_client")
    def test_main(self, mock_client):
        """
        Should exit clean after doing things

        Discord client async loop is mocked and not run but is tested that
        a call was made.
        """
        ec.DISCORD_TOKEN = "Do not show secrets in test"
        self.assertEqual(ec.main(), 0)
        mock_client.run.assert_called()
        mock_client.run.assert_called_with(ec.DISCORD_TOKEN)

    def test_join_ignore_me(self):
        """ On Joins should ignore bot actions """
        with patch("eggbot.eggbotcore.discord_client") as mock_client:
            mock_client.user.id = "123456789"
            # Create mocked member
            mock_member = unittest.mock.Mock()

            # ID is client, not a bot
            mock_member.bot = False
            mock_member.id = "123456789"
            self.assertFalse(run_loop(ec.on_member_join, mock_member))

            # ID is not client, not a bot
            mock_member.id = "987654321"
            self.assertTrue(run_loop(ec.on_member_join, mock_member))

            # ID is not client, is a bot
            mock_member.bot = True
            self.assertFalse(run_loop(ec.on_member_join, mock_member))

    def test_message_ignore_me(self):
        """ Message events should ignore bot chatter """
        with patch("eggbot.eggbotcore.discord_client") as mock_client:
            mock_client.user.id = "123456789"
            # Create mocked message
            mock_message = unittest.mock.Mock()

            # Id is client, not bot
            mock_message.author.id = "123456789"
            mock_message.author.bot = False
            self.assertFalse(run_loop(ec.on_message, mock_message))

            # ID is not client, not a bot
            mock_message.author.id = "987654321"
            self.assertTrue(run_loop(ec.on_message, mock_message))

            # ID is not client, is a bot
            mock_message.author.bot = True
            self.assertFalse(run_loop(ec.on_message, mock_message))

    def test_join_pub_events(self):
        """ Make sure join calls the "on_join" sub list """
        # TODO
        _join_sub_01 = unittest.mock.Mock()
        _join_sub_02 = unittest.mock.Mock()
        ec.eventSubs.sub_create(_join_sub_01, "on_join")
        ec.eventSubs.sub_create(_join_sub_02, "on_join")

        mock_member = unittest.mock.Mock()
        mock_member.id = "987654321"
        mock_member.bot = False

        with patch("eggbot.eggbotcore.discord_client") as mock_client:
            mock_client.user.id = "123456789"
            self.assertTrue(run_loop(ec.on_member_join, mock_member))

        _join_sub_01.assert_called_with(mock_member)
        _join_sub_02.assert_called_with(mock_member)

    def test_message_pub_events(self):
        """ Make sure messages call the "on_message" sub list """
        # TODO
        message_sub_01 = unittest.mock.Mock()
        message_sub_02 = unittest.mock.Mock()
        ec.eventSubs.sub_create(message_sub_01, "on_message")
        ec.eventSubs.sub_create(message_sub_02, "on_message")

        mock_message = unittest.mock.Mock()
        mock_message.author.id = "987654321"
        mock_message.author.bot = False

        with patch("eggbot.eggbotcore.discord_client") as mock_client:
            mock_client.userid = "123456789"
            self.assertTrue(run_loop(ec.on_message, mock_message))

        message_sub_01.assert_called_with(mock_message)
        message_sub_02.assert_called_with(mock_message)
