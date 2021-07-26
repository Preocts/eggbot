"""Constant Values used by the bot"""
import dataclasses

from secretbox import SecretBox

secretbox = SecretBox(auto_load=True)


@dataclasses.dataclass
class EggbotClient:
    """Client data"""

    name = "eggbot"
    desc = "eggbot: A bot made by an egg"
    prefix = "!"
    token = secretbox.get("EGGBOT_TOKEN")
    owner = secretbox.get("EGGBOT_OWNER", "123151368885239809")


@dataclasses.dataclass
class FilePaths:
    """Where are things located"""

    exts = "eggbot/exts"
