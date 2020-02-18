#Egg Bot

----
## Custom Discord Chat Bot
What started as a simple way to send a welcome message when a new user joined a guild, Egg Bot has expanded to include:

- Definable greetings, both DM and chat, for new user joins
- A custom, regex driven, alert system that watches for mentions of your choice called ShoulderBird
- Highly definable permission based chat commands
 - Control by Guild, Channels, Roles, and Users
 - more features in the works

Contact **Preocts#8196** on Discord for more info

----
## .env
Running this program requires you to create and define your own .env file with two keys.

```
DISCORD_TOKEN={API Secret Here}
BOT_OWNER={Your Discord ID here}
```

----
## base.egg

Configuration is done is JSON format with a base.egg file provided to get you started. It uses three main keys with sub keys to define the guild each applies to.

**Foreshadowing, these are all changing in 0.3 because they need to.**

**Version 0.2.2** - Sticky Egg configuration keys:


### guildConfig { "Guild Name": { "Options" } }

Options that do things in guildConfig:

- autowelcomeDM - Chat that is sent to a new join via DM
- autowelcomeDMImage - Optional image that will be posted to the DM **before** the chat*
- autowelcomeChat - Chat that is sent to the welcome channel listed below on new join
- autowelcomeChatImage - Optional image that will be posted to the channel **before** the chat*
- autowelcomeChannel - Where the bot is allowed to post welcome message. If blank the bot will not post to any channel.
- allowedChatRooms - Depreciated

*\*Image path starts in the same directory the code is running from*

### shoulderBird { "Guild name": { "User Name" : "Regex Search" } }

- This will search all incoming chats that the bot can see and look for the Regex expression
- If Regex finds a match, the chat is DM'ed to the User Name defined

### botCommands { "Guild name" : { "Trigger": { "Options" } } }

Options that do things in botCommands:

*These are all case sensitive*

- content : This is the bot's chat output when a command runs
- users : Restricts command to listed users
- roles : Restricts command to listed roles
- channels : Restricts command to listed channels
- action : triggers some hard-coded actions

*All listed values are comma separated with spaces*

*Example: "users" : "Preocts, NotPreocts, EggMan"*

**Actions**
- disconnect : Shuts connection down
  - *Can **only** be run by userID that matches BOT_OWNER in .env file regardless of options*

- edit-command : Creates or updates given command
  - *!trigger {Command Name} | {option1 = value} | {option2 = value} | {optionN = value}*

- delete-command : Deletes given command
  - *!trigger {Command Name}*

- get-command : Outputs the command in the same format it was created. Use this for copy/pasting commands or remembering how to format them
  - *!trigger {Command Name}*

- list-command : Lists all commands in guild.
  - *!trigger {Command Name}*