# -*- coding: utf-8 -*-
""" Test core entity objects """
import os
import pathlib
import random
import unittest

from eggbot.core_entities import CoreConfig


class TestCoreConfig(unittest.TestCase):
    def test_singleton(self):
        """ Once instance to rule them all """
        config = CoreConfig.get_instance()
        with self.assertRaises(Exception):
            _ = CoreConfig()
        second_config = CoreConfig.get_instance()
        self.assertIs(config, second_config)

    def test_exist(self):
        """ Unit Test """
        config = CoreConfig.get_instance()
        self.assertIsInstance(config, CoreConfig)
        self.assertIsInstance(config.config, dict)

    def test_abs(self):
        """ Unit Test """
        config = CoreConfig.get_instance()
        compare_path = __file__
        self.assertIsInstance(config.abs_path, str)
        self.assertTrue(config.abs_path.startswith(compare_path[0]))
        self.assertIn(config.abs_path, compare_path)

    def test_cwd(self):
        """ Unit Test """
        config = CoreConfig.get_instance()
        self.assertIsInstance(config.cwd, str)
        self.assertEqual(config.cwd, os.getcwd())

    def test_load(self):
        """ Unit Test """
        config = CoreConfig.get_instance()
        # Missing file
        config.load("invalid.file")
        self.assertIsInstance(config.config, dict)
        self.assertFalse(config.config)

        # Valid relative but invalid JSON
        config.load("README.md")
        self.assertIsInstance(config.config, dict)
        self.assertFalse(config.config)

        # Valid default
        config.load()
        self.assertIsInstance(config.config, dict)
        self.assertTrue(config.config)

        # Valid absolute
        filepath = pathlib.Path("./tests/files/mock_config.json").absolute()
        config.load(filepath, True)
        self.assertIsInstance(config.config, dict)
        self.assertTrue(config.config)

    def test_config_crud(self):
        """ Unit Test """
        random.seed()
        key = f"unitTest{random.randint(1000,10000)}"  # nosec
        config = CoreConfig.get_instance()
        config.load()

        self.assertTrue(config.create(key, "Test Value"))
        self.assertIn(key, config.config.keys())
        self.assertFalse(config.create(12345, "Test Value"))
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
        """ Unit Test """
        args_list = [
            (),
            (pathlib.Path("./tests/files/mock_config.json").absolute(), True),
        ]
        random.seed()
        key = f"unitTest{random.randint(1000,10000)}"  # nosec

        config = CoreConfig.get_instance()

        for args in args_list:
            config.load(*args)
            self.assertNotIn(key, config.config.keys())
            self.assertTrue(config.create(key, "Test Value"))
            self.assertTrue(config.save(*args))
            config.load(*args)
            self.assertIn(key, config.config.keys())
            self.assertTrue(config.delete(key))
            self.assertTrue(config.save(*args))
            config.load(*args)
            self.assertNotIn(key, config.config.keys())

    def test_unload(self):
        """ Empty current config """
        config = CoreConfig.get_instance()
        config.unload()
        self.assertEqual(config.config, {})
