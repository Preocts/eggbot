# eggbot - Discord Chat Bot

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
1. **done** Shoulder Bird plug-in refactor
1. **done** OnJoin module refactor
1. *started* Convert to pytest framework for unit tests
1. **done** Kudos module refactor
1. Coverage to minimum 90% - all files
1. Build a better roadmap
---

## Requirements

- Python >= 3.8
- discord.py >= 1.7.1

## Installation

**Pending re-write**


## Documentation

- [ShoulderBird Module](docs/shoulderbird.md)
- [JoinAction Module](docs/joinactions.md)
- [ChatKudos Module](docs/chatkudos.md)



## Environment setup

The bot is setup to pull secrets from a `.env` file located in the root of the project directory.  An empty `.env` is provided with place-holder notation.

.env
```ini
DISCORD_SECRET=[Bot token here]
```

## Tests

To run them:

```bash
(venv) $ pytest -v tests
```
