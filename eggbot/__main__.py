"""
Primary point of entry for eggbot, used to configure logging and invoke bot

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

    # eggbot.load_extension("eggbot.exts.testing")

    eggbot.run(constants.secretbox.get("EGGBOT_TOKEN"))

    return 0


if __name__ == "__main__":
    sys.exit(main())
