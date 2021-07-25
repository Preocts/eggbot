"""Constant Values used by the bot"""
import dataclasses

from secretbox import SecretBox

secretbox = SecretBox(auto_load=True)


@dataclasses.dataclass
class EggbotClient:
    """Client data"""

    name: str = "eggbot"
    desc: str = "eggbot: A bot made by an egg"
    prefix: str = secretbox.get("EGGBOT_PREFIX", "!")
    token: str = secretbox.get("EGGBOT_TOKEN")
    owner: str = secretbox.get("EGGBOT_OWNER", "123151368885239809")
