"""
Egg Bot, Discord Modular Bot

Author  : Preocts
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/eggbot
"""
# We are all only eggs
from typing import Any

import discord
from discord.ext import commands

from eggbot import constants


class EggbotCore(commands.Bot):
    """Core of the egg"""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


_intents = discord.Intents.all()

eggbot = EggbotCore(
    command_prefix=constants.EggbotClient.prefix,
    description=constants.EggbotClient.desc,
    intents=_intents,
)
