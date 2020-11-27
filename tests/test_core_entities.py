""" Test core entity objects """
import pathlib
import random
import unittest

from eggbot import core_entities


class TestCoreConfig(unittest.TestCase):

    def test_exist(self):
        config = core_entities.CoreConfig()
        self.assertIsInstance(config, core_entities.CoreConfig)
        self.assertIsInstance(config.config, dict)

    def test_abs(self):
        config = core_entities.CoreConfig()
        compare_path = core_entities.__file__
        self.assertIsInstance(config.abs_path, str)
        self.assertTrue(config.abs_path.startswith(compare_path[0]))
        self.assertIn(config.abs_path, compare_path)

    def test_load(self):
        config = core_entities.CoreConfig()

        # Missing file
        config.load('invalid.file')
        self.assertIsInstance(config.config, dict)
        self.assertFalse(config.config)

        # Valid relative but invalid JSON
        config.load('egg_bot.py')
        self.assertIsInstance(config.config, dict)
        self.assertFalse(config.config)

        # Valid default
        config.load()
        self.assertIsInstance(config.config, dict)
        self.assertTrue(config.config)

        # Valid absolute
        filepath = pathlib.Path('./tests/files/mock_config.json').absolute()
        config.load(filepath, True)
        self.assertIsInstance(config.config, dict)
        self.assertTrue(config.config)

    def test_config_crud(self):
        random.seed()
        key = f'unitTest{random.randint(1000,10000)}'
        config = core_entities.CoreConfig()
        config.load()

        self.assertTrue(config.create(key, 'Test Value'))
        self.assertIn(key, config.config.keys())
        self.assertFalse(config.create(12345, 'Test Value'))
        self.assertNotIn(12345, config.config.keys())
        self.assertFalse(config.create(key, 'Test Value'))

        self.assertEquals(config.read(key), 'Test Value')
        self.assertIsNone(config.read(key + '00'))

        self.assertTrue(config.update(key, 'New Value'))
        self.assertEquals(config.config.get(key), 'New Value')
        self.assertFalse(config.update(key + '00', 'New Value'))
        self.assertNotIn(key + '00', config.config.keys())

        self.assertTrue(config.delete(key))
        self.assertNotIn(key, config.config.keys())

    def test_save(self):
        args_list = [
            ('/config/eggbot.json', False),
            (pathlib.Path('./tests/files/mock_config.json').absolute(), True)
        ]
        random.seed()
        key = f'unitTest{random.randint(1000,10000)}'

        config = core_entities.CoreConfig()

        for args in args_list:
            print(f"Testing with: {args}")
            config.load(*args)
            self.assertNotIn(key, config.config.keys())
            self.assertTrue(config.create(key, 'Test Value'))
            self.assertTrue(config.save(*args))
            config.load(*args)
            self.assertIn(key, config.config.keys())
            self.assertTrue(config.delete(key))
            self.assertTrue(config.save(*args))
            config.load(*args)
            self.assertNotIn(key, config.config.keys())
            print("Completed")
