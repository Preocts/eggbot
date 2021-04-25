#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Testing suite """
import asyncio
import unittest
from unittest.mock import patch

from eggbot import eggbotcore as ec
from eggbot.eggbotcore import EggBotCore
from eggbot.models.eventtype import EventType


def run_loop(func, *args, **kwargs):
    """ Hack to test async functions """
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(func(*args, **kwargs))
    return result


class TestEggbotCore(unittest.TestCase):
    """ Testing suite """

    def test_attributes(self):
        """ These need to exist """
        eggbot = EggBotCore()
        self.assertIsInstance(eggbot.discord_, ec.DiscordClient)
        self.assertIsInstance(eggbot.event_subs, ec.EventSubs)
        self.assertIsInstance(eggbot.core_config, ec.ConfigFile)
        self.assertIsInstance(eggbot.env_vars, ec.LoadEnv)

    def test_config_load(self):
        """ Pass fail on config load """
        eggbot = EggBotCore()
        self.assertTrue(eggbot.load_config())
        with patch.object(eggbot.core_config, "load", return_value=False):
            self.assertFalse(eggbot.load_config())
        eggbot.core_config = None
        with self.assertRaises(Exception):
            eggbot.load_config()

    def test_launch_bot(self):
        """ Should exit clean after doing things """
        eggbot = EggBotCore()
        with patch.object(eggbot.discord_, "run") as mock_client:
            self.assertEqual(eggbot.launch_bot(), 0)
            mock_client.assert_called()

        with patch.object(eggbot, "load_config", return_value=False):
            with self.assertRaises(Exception):
                eggbot.launch_bot()

        eggbot.env_vars = None
        with self.assertRaises(Exception):
            eggbot.launch_bot()

    def test_join_ignore_me(self):
        """ On Joins should ignore bot actions """
        eggbot = EggBotCore()
        with patch.object(eggbot.discord_, "client") as mock_client:
            mock_client.user.id = "123456789"
            # Create mocked member
            mock_member = unittest.mock.Mock()

            # ID is client, not a bot
            mock_member.bot = False
            mock_member.id = "123456789"
            self.assertFalse(run_loop(eggbot.on_member_join, mock_member))

            # ID is not client, not a bot
            mock_member.id = "987654321"
            self.assertTrue(run_loop(eggbot.on_member_join, mock_member))

            # ID is not client, is a bot
            mock_member.bot = True
            self.assertFalse(run_loop(eggbot.on_member_join, mock_member))

    def test_message_ignore_me(self):
        """ Message events should ignore bot chatter """
        eggbot = EggBotCore()
        with patch.object(eggbot.discord_, "client") as mock_client:
            mock_client.user.id = "123456789"
            # Create mocked message
            mock_message = unittest.mock.Mock()

            # ID is client, not bot
            mock_message.author.id = "123456789"
            mock_message.author.bot = False
            self.assertFalse(run_loop(eggbot.on_message, mock_message))

            # ID is not client, not a bot
            mock_message.author.id = "987654321"
            self.assertTrue(run_loop(eggbot.on_message, mock_message))

            # ID is not client, is a bot
            mock_message.author.bot = True
            self.assertFalse(run_loop(eggbot.on_message, mock_message))

    def test_join_pub_events(self):
        """ Make sure join calls the "on_join" sub list """
        eggbot = EggBotCore()
        _join_sub_01 = unittest.mock.AsyncMock()
        _join_sub_02 = unittest.mock.AsyncMock()
        eggbot.event_subs.add(EventType.ON_MEMBER_JOIN, _join_sub_01)
        eggbot.event_subs.add(EventType.ON_MEMBER_JOIN, _join_sub_02)

        mock_member = unittest.mock.Mock()
        mock_member.id = "987654321"
        mock_member.bot = False

        with patch.object(eggbot.discord_, "client") as mock_client:
            mock_client.user.id = "123456789"
            self.assertTrue(run_loop(eggbot.on_member_join, mock_member))

        _join_sub_01.assert_called_with(mock_member)
        _join_sub_02.assert_called_with(mock_member)

    def test_message_pub_events(self):
        """ Make sure messages call the "on_message" sub list """
        eggbot = EggBotCore()
        message_sub_01 = unittest.mock.AsyncMock()
        message_sub_02 = unittest.mock.AsyncMock()
        eggbot.event_subs.add(EventType.ON_MESSAGE, message_sub_01)
        eggbot.event_subs.add(EventType.ON_MESSAGE, message_sub_02)

        mock_message = unittest.mock.Mock()
        mock_message.author.id = "987654321"
        mock_message.author.bot = False

        with patch.object(eggbot.discord_, "client") as mock_client:
            mock_client.userid = "123456789"
            self.assertTrue(run_loop(eggbot.on_message, mock_message))

        message_sub_01.assert_called_with(mock_message)
        message_sub_02.assert_called_with(mock_message)
