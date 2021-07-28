"""Tests for utils/tomlio.py"""
import os
import tempfile
from typing import Generator

import pytest

from eggbot.utils import tomlio

TOML_CONTENTS = [
    "[default]",
    'test1="roger"',
    'test2="rogerroger"',
]

EXPECTED_TOML = {
    "default": {
        "test1": "roger",
        "test2": "rogerroger",
    }
}


@pytest.fixture(scope="function", name="toml_load")
def fixture_toml_load() -> Generator[str, None, None]:
    """Builds a mock toml to load"""
    try:
        file_desc, path = tempfile.mkstemp()
        with os.fdopen(file_desc, "w", encoding="utf-8") as temp_file:
            temp_file.write("\n".join(TOML_CONTENTS))
        yield path
    finally:
        os.remove(path)


@pytest.fixture(scope="function", name="toml_save")
def fixture_toml_save() -> Generator[str, None, None]:
    """Creates a file to save into"""
    try:
        _, path = tempfile.mkstemp()
        yield path
    finally:
        os.remove(path)


def test_missing_file() -> None:
    """Can't open a file that isn't there"""
    with pytest.raises(FileNotFoundError):
        tomlio.load("")


def test_invalid_toml() -> None:
    """Can't load a non-toml"""
    with pytest.raises(ValueError):
        tomlio.load("tests/tomlio_test.py")


def test_toml_load(toml_load: str) -> None:
    """Load a TOML file"""
    results = tomlio.load(toml_load)

    assert results == EXPECTED_TOML


def test_path_not_found() -> None:
    """Can't save to a directory that doens't exist"""
    with pytest.raises(FileNotFoundError):
        tomlio.save("./8675309_call_now/nofile.txt", EXPECTED_TOML)


def test_not_valid_data(toml_save: str) -> None:
    """Can't save invalid data"""
    with pytest.raises(TypeError):
        tomlio.save(toml_save, "this will fail")  # type: ignore


def test_save_and_load(toml_save: str) -> None:
    """Save a toml and load to confirm"""
    tomlio.save(toml_save, EXPECTED_TOML)

    result = tomlio.load(toml_save)

    assert result == EXPECTED_TOML
