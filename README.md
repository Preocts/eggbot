# Egg_bot
### Custom Discord Chat Bot

The goal of this chat bot is to provide basic funcationallity to
select discord channels.  The bot will be private and invites handled
by Preocts on a case by case basis.

Initial version goals include, but are not limited to,
    - Greeting new members on joining a Guild
    - Command controlled disconnect
    - Alais monitoring with DM alerts
    
    Contact Preocts#8196 for more info

### Egg Configuration File
White space is ignore.
Lines that don't start with a **Key** will be lost on next load/save.

**Keys:**
"@" starts a guild configuration.
  Each guild line must be unique
"&" adds configuration option to most recently listed Guide
  Egg Bot will import everything, attempt to use it, fall-back to defaults if it is wrong

**Special:**
  These can be used in text the bot will display such as welcome messages and response commands
- [MENTION] = replaced with @name to mention member
- [USERNAME] = replaced with display name of member (nickname/default if no nick is set)
- [GUILDNAME] = replaced with Guild name if available (doesn't work if event is from DMs)
