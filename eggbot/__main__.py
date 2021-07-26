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


def main() -> int:
    """Main entry point"""
    logging.basicConfig(level="INFO")

    # TODO: extension loader
    # eggbot.load_extension("eggbot.exts.temp_testing")

    eggbot.run(constants.secretbox.get("EGGBOT_TOKEN"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
