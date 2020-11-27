""" Egg Bot, Discord Modular Bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging

from eggbot import core_entities


logger = logging.getLogger(__name__)
eggbot_config = core_entities.CoreConfig()


def load_config() -> bool:
    eggbot_config.load()
    if not eggbot_config.config:
        return False
    return True

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
