# -*- coding: utf-8 -*-
""" Test core entity objects """
import random
import unittest

from eggbot.configfile import ConfigFile


class TestCoreConfig(unittest.TestCase):
    """Test suite"""

    def test_properties(self):
        """Unit Test"""
        config = ConfigFile("./tests/fixtures/mock_config.json")
        config.load()
        self.assertIsInstance(config.config, dict)

    def test_load(self):
        """Unit Test"""
        config = ConfigFile("./tests/fixtures/mock_config.json")
        # Missing file
        config.load("invalid.file")
        self.assertFalse(config.config)

        # Valid relative but invalid JSON
        config.load("README.md")
        self.assertFalse(config.config)

        # Valid default
        config.load()
        self.assertFalse(config.config)

    def test_config_crud(self):
        """Unit Test"""
        random.seed()
        key = f"unitTest{random.randint(1000,10000)}"  # nosec
        config = ConfigFile("./tests/fixtures/mock_config.json")

        self.assertTrue(config.create(key, "Test Value"))
        self.assertIn(key, config.config.keys())
        self.assertFalse(config.create(12345, "Test Value"))  # type: ignore
        self.assertNotIn(12345, config.config.keys())
        self.assertFalse(config.create(key, "Test Value"))

        self.assertEqual(config.read(key), "Test Value")
        self.assertIsNone(config.read(key + "00"))

        self.assertTrue(config.update(key, "New Value"))
        self.assertEqual(config.config.get(key), "New Value")
        self.assertFalse(config.update(key + "00", "New Value"))
        self.assertNotIn(key + "00", config.config.keys())

        self.assertTrue(config.delete(key))
        self.assertNotIn(key, config.config.keys())
        self.assertFalse(config.delete(key))

    def test_save(self):
        """Unit Test"""
        random.seed()
        key = f"unitTest{random.randint(1000,10000)}"  # nosec

        config = ConfigFile("./tests/fixtures/mock_config.json")
        config.load()
        self.assertTrue(config.config)

        self.assertNotIn(key, config.config.keys())
        self.assertTrue(config.create(key, "Test Value"))
        self.assertTrue(config.save())

        self.assertIn(key, config.config.keys())
        self.assertTrue(config.delete(key))
        self.assertTrue(config.save())

        self.assertNotIn(key, config.config.keys())
        self.assertTrue(config.config)

    def test_unload(self):
        """Empty current config, reload from same file"""
        config = ConfigFile("./tests/fixtures/mock_config.json")
        config.load()
        self.assertTrue(config.config)
        config.unload()
        self.assertEqual(config.config, {})
        config.load()
        self.assertTrue(config.config)
