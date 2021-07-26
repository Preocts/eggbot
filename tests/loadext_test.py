"""Tests for utils/loadext.py"""
from pathlib import Path

from eggbot.utils import loadext

MOCK_FILE = Path("tests/fixtures/ext/valid.py")
EXPECTED_FILE = "tests.fixtures.ext.valid"
EXPECTED_FILES = [
    Path("tests/fixtures/ext/valid.py"),
    Path("tests/fixtures/ext/invalid.py"),
    Path("tests/fixtures/ext/__init__.py"),
]

MOCK_EXT = "tests/fixtures/ext"
EXPECTED_EXT = ["tests.fixtures.ext.valid"]


def test_load_ext() -> None:
    """Run against mock ext in fixtures"""
    result = loadext.load_ext(MOCK_EXT)

    assert result == EXPECTED_EXT


def test_get_files() -> None:
    """Use pathlib to get all .py files"""
    result = loadext.get_files(MOCK_EXT)

    assert result == EXPECTED_FILES


def test_convert_to_module_path() -> None:
    """turn a file path into an import path"""
    result = loadext.convert_to_module_path(MOCK_FILE)

    assert result == EXPECTED_FILE
