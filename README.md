# Egg Bot

Egg Bot is a side-project Discord chat bot written for a friend that just keeps me entertained.

Currently under a re-write.

---

## Road map

1. **done** Basic configuration loading
1. **done** Secret loading
1. **done** Connection to discord (doesn't do anything)
1. **done** Refactor to class objects
1. **done** Event subscription abstract layer
   - Frame-work for plug-ins (modules) to be called on discord client events
1. **done** Refactor discord client into abstract layer
1. Documentation update for setup, installation
1. Packaging scripts
1. Logging configuration on launch
   - Rotating file output
   - Console output
1. **done** Further abstraction of Discord client - Events and Cogs
1. Shoulder Bird plug-in refactor
1. Convert to pytest framework for unit tests
1. Build a better roadmap
1. Kudos plug-in refactor

---

## Requirements

- Python >= 3.8
- discord.py >= 1.5.1

## Installation

**Pending re-write**

## Environment setup

The bot is setup to pull secrets from a `.env` file located in the root of the project directory.  An empty `.env` is provided with place-holder notation.

.env
```ini
DISCORD_SECRET=[Bot token here]
```

## Tests

Tests are written using Python's build-in `unittest`. To run them:

```bash
(venv) $ python -m unittest discover tests

or

(venv) $ pytest -v tests
```
