#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" JSON Config input and output

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import json
import logging

from typing import Optional


class ConfigIO:
    """ Input and output abstract layer for JSON configs """

    logger = logging.getLogger(__name__)

    def load(self, filename: Optional[str] = None) -> dict:
        """ Loads a config json, dumps loaded config with no prompt """
        loaded_config: dict = {}
        if not filename:
            self.logger.error("No filename provided to load, aborting.")
            return loaded_config
        try:
            with open(filename, "r", encoding="UTF-8") as input_file:
                loaded_config = json.loads(input_file.read())
        except (FileNotFoundError, IsADirectoryError):
            self.logger.error(".load() Configuration file not found at %s", filename)
        except json.decoder.JSONDecodeError:
            self.logger.error(
                ".load() Configuration file empty or formatted incorrectly, that's "
                "sad. You can get a new one at: https://github.com/Preocts/Egg_Bot"
            )
        except OSError as err:
            self.logger.error(".load() Something failed loading configuations: %s", err)
            self.logger.error("", exc_info=True)
        return loaded_config

    def save(self, config: dict, filename: Optional[str] = None) -> bool:
        """ Saves a config json, overwrites existing file with no prompt """
        if not filename:
            self.logger.error("No filename provided to save, aborting.")
            return False
        try:
            with open(filename, "w", encoding="UTF-8") as out_file:
                out_file.write(json.dumps(config, indent=4) + "\n")
        except OSError as err:
            self.logger.error(".save() Cannot save core config: %s", err)
            self.logger.error("", exc_info=True)
            return False
        return True
