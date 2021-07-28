"""
IO functions for TOML config files

Author  : Preocts
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/eggbot
"""
import logging
import pathlib
from typing import Any
from typing import Dict

import toml


logger = logging.getLogger("TOMLHandler")


def load(filepath: str) -> Dict[str, Any]:
    """Load a TOML file"""

    if not pathlib.Path(filepath).is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as infile:
        try:
            loaded = toml.load(infile)
        except toml.TomlDecodeError as err:
            raise ValueError("Expected TOML format") from err

    return dict(loaded)


def save(filepath: str, data: Dict[str, Any]) -> None:
    """Save a TOML file"""

    if not pathlib.Path(filepath).parent.is_dir():
        raise FileNotFoundError(f"Path not found: {filepath}")

    with open(filepath, "w", encoding="utf-8") as outfile:
        try:
            toml.dump(data, outfile)
        except TypeError as err:
            raise TypeError("Cannot format as TOML") from err
