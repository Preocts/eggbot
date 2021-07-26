"""Sanity checks against certain constants"""
import pathlib

from eggbot import constants


def test_path_exists() -> None:
    """Watch for mistakes in path names"""

    assert pathlib.Path(constants.FilePaths.exts).is_dir
