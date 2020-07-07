# Egg_Bot - A Discord Chat Bot

Created by Preocts

Preocts#8196 Discord | [Github](https://github.com/Preocts/Egg_Bot)

---

**Requirements**
- [Python 3.8.1](https://www.python.org/)
- [discordpy v1.3.2](https://github.com/Rapptz/discord.py)
- [pyhton-dotenv](https://github.com/theskumar/python-dotenv)

---

## Customizable Discord Chat Bot

The idea behind Egg_Bot's core code is to have a very slim script that is powered by Discord.py but can be enhanced with modules. The script will attempt to auto-load any .py file found in the ./modules path and integrate configured events for that module. 

Each module, in a sense, is its own bot responding to the event feed from the core script. 

What started as a simple way to send a welcome message when a new user joined a guild, Egg Bot has expanded to include:

- Core Discord bot that listens to events flows from On Messages, On Join, and On Typing
- Auto module loading for plugin of features around these events including and not limited too:
  - Definable greetings, both DM and chat, for new user joins
  - A custom, regex driven, alert system that watches for mentions of your choice called ShoulderBird
  - Highly definable permission based chat commands
    - Control by Guild, Channels, Roles, and Users
  - Bot Guard - an allow list for bots that kicks unexpected bots to reduce noise/spam/scams
  - Chat Kudos - Karma from IRC and HipChat is born again
  - more features in the works

----

## Installation

Running this program requires you to create and define your own .env file with two keys.

.env

```ini
DISCORD_TOKEN={API Secret Here}
BOT_OWNER={Your Discord ID here}
```

ToDo: More instructions to be written

---

## Released Modules

* [Chat Kudos](https://github.com/Preocts/Egg_Bot/blob/source/docs/chatKudos.md)
* [Shoulder Bird](https://github.com/Preocts/Egg_Bot/blob/source/docs/shoulderBird.md)