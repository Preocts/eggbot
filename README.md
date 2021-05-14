# eggbot - Discord Chat Bot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/eggbot/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/eggbot/main)
[![Python package](https://github.com/Preocts/eggbot/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/eggbot/actions/workflows/python-tests.yml)


Egg Bot is a side-project Discord chat bot written for a friend that just keeps me entertained. It is designed to be module-based with a super light-weight core and the ability to add event calls to external modules with no code changes.

Check the [road-map](README.md#Roadmap) for an idea on where the current re-write is with this goal.

## Module Documentation

- [Creating a Module](docs/module_setup.md) - How to create a module that will auto-load
- [ShoulderBird Module](docs/shoulderbird.md) - Get a direct-message notification on keywords
- [JoinAction Module](docs/joinactions.md) - Say hello to new joiners
- [ChatKudos Module](docs/chatkudos.md) - Nothing spells discord like an arbitrary point system!

---

## Requirements

- [Python >= 3.8](https://www.python.org/downloads/)
- [Discord.py >= 1.7.1](https://github.com/Rapptz/discord.py)

---

## Installation

Current installation is simply running the code out of a working directory.

1. Clone the repository to your computer and enter that directory:
```bash
$ git clone https://github.com/Preocts/eggbot.git

$ cd eggbot
```

2. Create a Python `venv` (optional but highly recommended):
```bash
$ python3 -m venv venv
```

3. Activate the `venv`
```bash
# For Linux/Mac
$ source ./venv/bin/activate

# For Command line/Powershell
$ venv\Scripts\activate.bat
```

4. Update pip and install `requirements.txt`
```bash
$ pip install --upgrade pip setuptools wheel
$ pip install -r requirements.txt
```

5. Edit the `.env` file and replace the placeholder text with your bot's Discord Token and your Discord account ID.
```env
DISCORD_SECRET=[BOT DISCORD API TOKEN]
BOT_OWNER=[YOUR DISCORD ID]
```

6. Launch the bot
```bash
$ python3 -m eggbot
```

---

## Roadmap

1. Logging configuration on launch
   - Rotating file output
   - Console output
1. Convert to pytest framework for unit tests
1. Coverage to minimum 90% - all files
1. Packaging scripts
1. Build a better roadmap
1. **done** Frame-work for plug-ins (modules) to be called on discord client events
1. **done** Auto-module loader with even registration
1. **done** Basic configuration loading
1. **done** Secret loading
1. **done** Connection to discord (doesn't do anything)
1. **done** Refactor to class objects
1. **done** Event subscription abstract layer
1. **done** Refactor discord client into abstract layer
1. **done** Documentation update for setup, installation
1. **done** Further abstraction of Discord client - Events and Cogs
1. **done** Shoulder Bird plug-in refactor
1. **done** OnJoin module refactor
1. **done** Kudos module refactor
