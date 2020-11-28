# Egg_Bot

[![Build Status](https://travis-ci.org/Preocts/Egg_Bot.svg?branch=main)](https://travis-ci.org/Preocts/Egg_Bot)

Primary Author: Preocts 

Find me on Discord: Preocts#8196  (just mention this repo)

[Github - https://github.com/Preocts/Egg_Bot](https://github.com/Preocts/Egg_Bot)

---

**Requirements**
- [Python>=3.8](https://www.python.org/)
- [discordpy>=1.5.1](https://github.com/Rapptz/discord.py)
- [pyhton-dotenv>=0.15.0](https://github.com/theskumar/python-dotenv)

**Enviromental Variable Requirements**

These are needed in either a `.env` file located in the `./eggbot` folder or to be set as an env variable through your launching/deployment scripts.

```
discord_api_key=[Discord Token]
owner_id=[Your Discord ID]
```


---

## Rebuild time

After ten months, 900+ commits, and 25k+ lines of python code I've learned so much more than I ever thought I would. Thanks 2020. 

Egg_bot has some great potential and now I feel up to delivering on it.

We start again! Back to the old road! 

---

## Roadmap

Check the [CHANGELOG](CHANGELOG.md) for more details

### Working on it - 

- Standing egg_bot.py back up after tearing all the structure down
- Dynamic module loading through decorator
- Test driven (re?)development

### Coming soon

- Shoulder Bird module for getting DM pings when someone mentions a keyword

### On the board

- Full recovery to where we were

### Known Issues

- `make install` will bury config files. Files are lost on reinstall. Need to find a solution allowing config files to remain accessible between installs.

---

If you want the old code it is stored in the completely mis-leading branch `working`

# Installation
The installation instructions below make use of a Makefile for running commands. If the OS you are using does not have `make` the commands referenced can be run directly from the command-line.

### Clone this Repo

```bash
git clone https://github.com/Preocts/Egg_Bot.git
cd Egg_Bot
```

### Install a `venv`.

It is highly recommended to always use a virtual environment when working with Python. This will keep library versions aligned between project and avoid other issues.

```bash
python3.8 -m venv venv
```

### Activate the `venv`. 

**Linux/Mac**:
```bash
source ./venv/bin/activate
```

**Windows**:
```dos
.\venv\Scripts\activate.bat
```

Your shell prompt should now be prefixed with a `(venv)`

### Install Egg_Bot

```bash
make install
```

### Start Egg_Bot

```bash
start-eggbot
```

---

### Run Unit tests

```bash
make test
```

### Update requirement files

```bash
make update
```

### Zip package for deployable

This will create `artifact.zip` in the root of the working directory. Packaged with the zip are all vendor libraries. `main.py` will be in the root directory of the zip, as point-of-entry for the program.

```bash
make package
```