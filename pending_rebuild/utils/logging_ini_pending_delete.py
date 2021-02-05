# -*- coding: utf-8 -*-
"""
So that I never have to remember how to initialize logging to my preferences

Built during 100DaysofCode.

Coded by: Preocts
    Discord: Preocts#8196
    GitHub: https://github.com/Preocts/eggUtils
"""

import json
import pathlib
import logging
import logging.config

logger = logging.getLogger(__name__)  # Create module level logger


def config_logger(
    filename: str = "./egglog/egglogging.json", log_level: str = "DEBUG"
) -> bool:
    """
    Loads a configuration from JSON and sets logging level

    Args:
        [str] : Path and name of the CONF file. Default ./egglogging.json
        [str] : Logging level to use. Default: DEBUG

    Returns:
        [bool] : Success or fail on loading config

    Raises:
        None
    """

    VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    pathlib.Path("./logs").mkdir(exist_ok=True)
    if not (log_level in VALID_LOG_LEVELS):
        log_level = "DEBUG"
    try:
        with open(filename) as file_:
            logConfig = json.load(file_)

    except FileNotFoundError:
        print(filename)
        print("SOMETHING BROKE")
        exit()
        logging.basicConfig(level=logging.DEBUG)
        logging.critical("CRITICAL: Config not found/valid for logger")
        logging.error("Exception occured", exc_info=True)
        logging.error("basicConfig loaded for logging_init. Not eggcellent!")
        return False

    if log_level != "DEBUG":
        for hands in logConfig["handlers"]:
            logConfig["handlers"][hands]["level"] = log_level

    logging.config.dictConfig(logConfig)
    logger = logging.getLogger()

    logger.info("Success: Logging configuration loaded and initialized")
    return True
