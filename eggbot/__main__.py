"""
Primary point of entry to start bot, load cogs, and config logging

Author  : Preocts
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/eggbot
"""
import logging
import sys

from eggbot import constants
from eggbot.eggbotcore import eggbot
from eggbot.utils import loadext


def main() -> int:
    """Main entry point"""
    logging.basicConfig(level="INFO")
    for ext in loadext.load_ext(constants.FilePaths.exts):
        eggbot.load_extension(ext)
    eggbot.run(constants.secretbox.get("EGGBOT_TOKEN"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
