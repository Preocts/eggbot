#!/usr/bin/env python3.8
""" Primary point of entry for Egg_Bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
import sys

from eggbot.eggbotcore import EggBotCore


def main() -> int:
    """ Main entry point """
    logging.basicConfig(level="INFO")

    eggbot = EggBotCore()

    eggbot.launch_bot()

    return 0


if __name__ == "__main__":
    sys.exit(main())
