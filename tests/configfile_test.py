"""Tests for configfile.py"""
import random

from eggbot.configfile import ConfigFile


def test_properties() -> None:
    """Unit Test"""
    config = ConfigFile("./tests/fixtures/mock_config.json")
    config.load()
    assert isinstance(config.config, dict)


def test_load() -> None:
    """Unit Test"""
    config = ConfigFile("./tests/fixtures/mock_config.json")
    # Missing file
    config.load("invalid.file")
    assert not config.config

    # Valid relative but invalid JSON
    config.load("README.md")
    assert not config.config

    # Valid default
    config.load()
    assert not config.config


def test_config_crud() -> None:
    """Unit Test"""
    random.seed()
    key = f"unitTest{random.randint(1000,10000)}"  # nosec
    config = ConfigFile("./tests/fixtures/mock_config.json")

    assert config.create(key, "Test Value")
    assert key in config.config.keys()
    assert not config.create(12345, "Test Value")  # type: ignore
    assert 12345 not in config.config.keys()
    assert not config.create(key, "Test Value")

    assert config.read(key) == "Test Value"
    assert config.read(key + "00") is None

    assert config.update(key, "New Value")
    assert config.config.get(key) == "New Value"
    assert not config.update(key + "00", "New Value")
    assert key + "00" not in config.config.keys()

    assert config.delete(key)
    assert key not in config.config.keys()
    assert not config.delete(key)


def test_save() -> None:
    """Unit Test"""
    random.seed()
    key = f"unitTest{random.randint(1000,10000)}"  # nosec

    config = ConfigFile("./tests/fixtures/mock_config.json")
    config.load()

    assert config.config

    assert key not in config.config.keys()
    assert config.create(key, "Test Value")
    assert config.save()

    assert key in config.config.keys()
    assert config.delete(key)
    assert config.save()

    assert key not in config.config.keys()
    assert config.config


def test_unload() -> None:
    """Empty current config, reload from same file"""
    config = ConfigFile("./tests/fixtures/mock_config.json")
    config.load()

    assert config.config

    config.unload()

    assert config.config == {}

    config.load()

    assert config.config
