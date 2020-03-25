""" Initialize standard logging configs for Egg Bot

    Typical Usage:
        import logging_init

        logger = logging.getLogger(__name__)  # Create Module Level Logger

        def main():
            logging_init.logINIT()

    Configuration File:
        ../config/logging_config.json
"""

import json
import logging
import logging.config


def logINIT():
    try:
        with open("config/logging_config.json") as file:
            logConfig = json.load(file)

    except FileNotFoundError:
        logging.basicConfig(filename='logs/BROKEN.log', level=logging.ERROR)
        logging.critical('CRITICAL: Config not found/valid for logger')
        logging.error('Exception occured', exc_info=True)
        logging.error('basicConfig loaded for logging_init. Not ideal!')
        return False

    logging.config.dictConfig(logConfig)
    logger = logging.getLogger(__name__)

    logger.info('Success: Logging configuration loaded and initialized')
    return True
