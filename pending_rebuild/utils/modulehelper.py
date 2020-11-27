""" Helper module containing useful tools for addon modules

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import os
import json
import logging
import pathlib

from eggbot.utils import logdec


logger = logging.getLogger(__name__)


class EggModuleException(Exception):
    """ Custom expection handler """

    def __init__(self, message: str = "Someone didn't define their exception"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


@logdec.debug_log
def loadjson(filepath: str) -> dict:
    """ Loads a json file from given path and returns a dict

    Please keep in mind the filepath is relative to the location of where
    eggbot.py is executed, not the path where the module resides.

    Args:
        filepath: Path and filename of json to load

    Returns:
        Dict
        If the file fails to load the return will contain: {'loadfail': True}
    """
    file_check = pathlib.Path(filepath)
    if not file_check.is_file():
        return {}

    json_file = {'loadfail': True}

    try:
        with open(filepath, 'r') as load_file:
            json_file = json.load(load_file)
    except json.decoder.JSONDecodeError:
        logger.error('Config file empty or bad format. ', exc_info=True)
    except FileNotFoundError:
        logger.error(f'Config file not found: {filepath}', exc_info=True)
    except Exception:
        logger.error(f'Unexpected error loading: {filepath}', exc_info=True)

    return json_file


@logdec.debug_log
def savejson(filepath: str, dict_: dict, formatted: bool = True) -> bool:
    """ Saves a json file to the given path and returns a bool

    Please keep in mind the filepath is relative to the location of where
    eggbot.py is executed, not the path where the module resides.
    Note: Will not hesitate to overwrite existing files.

    Args:
        filepath: Path and filename to save
        dict_: Python dictionary object to save
        formatted: If true the json file will be formatted with indents
    """
    saved = True
    sep = os.path.sep
    path = pathlib.Path(f'{sep}'.join(filepath.split(sep)[:-1]))
    path.mkdir(parents=True, exist_ok=True)

    try:
        with open(filepath, 'w') as save_file:
            save_file.write(json.dumps(dict_, indent=4))
    except (OSError, Exception):
        logger.error(f'File not be saved: {filepath}', exc_info=True)
        saved = False

    return saved
