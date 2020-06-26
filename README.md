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

## .env
Running this program requires you to create and define your own .env file with two keys.

```
DISCORD_TOKEN={API Secret Here}
BOT_OWNER={Your Discord ID here}
```
