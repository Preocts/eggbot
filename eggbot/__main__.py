#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
""" Primary point of entry for Egg_Bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import sys

from eggbot.eggbotcore import EggBotCore
from eggbot.models.eventtype import EventType
from modules.shoulderbirdparser import ShoulderBirdParser
from modules.joinactions import JoinActions


def main() -> int:
    """ Main entry point """
    eggbot = EggBotCore()

    # TODO: Replace with module loader
    # Register modules
    shoulderbird = ShoulderBirdParser()
    joinactions = JoinActions()

    eggbot.event_subs.add(EventType.MESSAGE, shoulderbird.onmessage)
    eggbot.event_subs.add(EventType.MEMBERJOIN, joinactions.onjoin)

    eggbot.launch_bot()

    # TODO: Replace with module unloader
    shoulderbird.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
