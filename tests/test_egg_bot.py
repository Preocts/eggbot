import unittest

from eggbot import eggbot_core
from eggbot import core_entities


class TestEggbotCore(unittest.TestCase):

    def test_config_load(self):
        self.assertTrue(eggbot_core.load_config())
        self.assertIsInstance(eggbot_core.eggbot_config, 
                              core_entities.CoreConfig)
        self.assertIsNotNone(eggbot_core.eggbot_config.config)
