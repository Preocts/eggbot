""" Decorators for logging function entrance and exit

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging


logger = logging.getLogger(__name__)


def debug_log(function):
    def wrapper(*args, **kwargs):
        logger.debug(f"[START] {function.__name__}, {args}, {kwargs}")
        return_value = function(*args, **kwargs)
        logger.debug(f"[STOP] {function.__name__}, {return_value}")
        return return_value

    return wrapper
