""" Entity objects for the core bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import json
import logging
import random

import dotenv


logger = logging.getLogger(__name__)
dotenv.load_dotenv()
random.seed()


class ProgramConfig(object):
    """ Base Program Config

    Keyword Args:
        filename [str]:
            If provided this will override loading the default configuration
            file expected at './config/eggbot.json'
    """

    def __init__(self, **kwargs):
        defaultconfig = './config/eggbot.json'
        self.config_file = kwargs.get('filename', defaultconfig)
        self.eggConfig = {}

    def load_config(self):
        file_body = open(self.config_file, 'r').read()
        try:
            self.eggConfig = json.loads(file_body)
        except json.decoder.JSONDecodeError:
            logger.critical('Configuration file empty or formatted '
                            'incorrectly, that\'s sad. You can get a new one '
                            'over at: https://github.com/Preocts/Egg_Bot')
            exit()
        except (OSError, Exception):
            logger.critical('Something went wrong loading configuations...')
            logger.critical('', exc_info=True)
            exit()
        return

    def save_config(self):
        try:
            open(self.config_file, 'w').write(json.dumps(self.eggConfig))
        except Exception as err:
            logger.error(f'Cannot save core config: {err}')
            logger.error('', exc_info=True)
        return

    def listening_to(self):
        """ Returns a random value from listening_to list """
