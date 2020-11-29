""" Entity objects for the core bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import json
import os
import logging
import pathlib
import typing

import dotenv


logger = logging.getLogger(__name__)
dotenv.load_dotenv()


class CoreConfig(object):
    """ Core configuration handler """

    def __init__(self, **kwargs):
        self.__abs_path = f"{os.path.sep}".join(
            __file__.split(os.path.sep)[0:-1]
        )
        self.__cwd = os.getcwd()
        self.__config = {}

    @property
    def abs_path(self) -> str:
        return self.__abs_path

    @property
    def cwd(self) -> str:
        return self.__cwd

    @property
    def config(self) -> dict:
        return dict(self.__config)

    def load(
        self,
        filepath: str = "./config/eggbot_core.json",
        abs_path: bool = False,
    ) -> bool:
        """Loads a config json

        Args:
            filepath: If provided this will override loading the default
                configuration file expected at './config/eggbot.json'
            abs_path: If True the filepath provided is treated as an
                absolute path. Otherwise the path is considered
                relative to this module
        """
        self.__config = {}
        rel_path = pathlib.Path(self.cwd).joinpath(filepath)
        path = filepath if abs_path else rel_path.resolve()

        try:
            with open(path, "r") as input_file:
                self.__config = json.loads(input_file.read())

        except (FileNotFoundError, IsADirectoryError):
            logger.error(f".load() Configuration file not found at: {path}")

        except json.decoder.JSONDecodeError:
            logger.error(
                ".load() Configuration file empty or formatted "
                "incorrectly, that's sad. You can get a new one "
                "over at: https://github.com/Preocts/Egg_Bot"
            )
            return False

        except (OSError, Exception):
            logger.error(
                ".load() Something went wrong loading configuations..."
            )
            logger.error("", exc_info=True)
            return False

        return True

    def save(
        self,
        filepath: str = "./config/eggbot_core.json",
        abs_path: bool = False,
    ) -> bool:
        """Saves a config json

        !Destructive save! Will not prevent overwriting existing files.

        Args:
            filepath: If provided this will override loading the default
                configuration file expected at './config/eggbot.json'
            abs_path: If True the filepath provided is treated as an
                absolute path. Otherwise the path is considered
                relative to this module
        """
        rel_path = pathlib.Path(self.cwd).joinpath(filepath)
        path = filepath if abs_path else rel_path.resolve()
        try:
            with open(path, "w") as out_file:
                out_file.write(json.dumps(self.__config, indent=4))
        except Exception as err:
            logger.error(f".save() Cannot save core config: {err}")
            logger.error("", exc_info=True)
            return False
        return True

    def read(self, key: str) -> typing.Any:
        """ Reads values by key from config. Returns None if not exists """
        return self.__config.get(key)

    def create(self, key: str, value: typing.Any = None) -> bool:
        """ Creates a key/value pair in the configuration """
        if not isinstance(key, str):
            logger.error(f".create() key not string. Given a {type(key)}")
            return False
        if key in self.config.keys():
            logger.error(".create() key already exists, use .update()")
            return False
        self.__config[key] = value
        return True

    def update(self, key: str, value: typing.Any = None) -> bool:
        """ Updates key/value pair in the configuration """
        if key not in self.__config.keys():
            logger.error(".update() key not found, use .create()")
            return False
        self.__config[key] = value
        return True

    def delete(self, key: str) -> bool:
        """ Deletes key from configuration """
        if key not in self.__config.keys():
            logger.error(".delete() key not found.")
            return False
        del self.__config[key]
        return True
