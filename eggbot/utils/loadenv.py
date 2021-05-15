#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Load a local .env file into environment

    Reads, parses, and inserts environmental variables from a .env
    file located within the working directory or provided path.

    Values loaded exist within the namespace of the python program
    only and do not alter the OS once the program ends

Author  : Preocts <preocts@preocts.com>
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""
import logging
import os
from typing import Dict
from typing import Optional


class LoadEnv:
    """ Load a local .env file into environment """

    logger = logging.getLogger(__name__)

    @staticmethod
    def get(key: str) -> str:
        """ Get a value from environ """
        return os.environ.get(key, "")

    def __init__(self) -> None:
        """ Provide a path to .env if not located in working directory """
        self.filepath: Optional[str] = None
        self.env_values: Dict[str, str] = {}

    def __del__(self):
        """ Destructor """
        if self.env_values:
            for key in self.env_values:
                del os.environ[key]

    def load(self, filepath: Optional[str] = None) -> None:
        """ Loads local .env or from path if provided """
        path = filepath if filepath else "./"
        if not os.path.isfile(os.path.join(path, ".env")):
            return
        try:
            with open(os.path.join(path, ".env"), "r", encoding="utf-8") as input_file:
                self.__parse_env(input_file.read())
        finally:
            self.__load_to_environ()

    def __parse_env(self, input_file: str) -> None:
        """ Parses env file into key-pair values """
        for line in input_file.split("\n"):
            if not line or line.strip().startswith("#") or len(line.split("=", 1)) != 2:
                # Blank line | Comment line | Unhealthy line
                continue
            key, value = line.split("=", 1)
            self.env_values[key.strip()] = value.strip()

    def __load_to_environ(self) -> None:
        """ Loads values to local environ """
        for key, value in self.env_values.items():
            os.environ[key] = value
