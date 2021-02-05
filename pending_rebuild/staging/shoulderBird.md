# Shoulder Bird Module v1.0.0

### Keyword pings, because sleep is not an option.

Shoulder Bird is the answer to "Can I get a ping when someone says [whatever] in the chat so that I'm aware?  The answer, my friends, is yes. Yes you can.

Shoulder Bird works on a regex engine that scans all chat that the bot can see for anything that matches the regex expression defined per user. A user, through DM command line option, can set their own regex expression for any guild that the bot is active in.  Once set, the bot will check that regex against any on_message events seen in the guild.

Fair warning, I'm aware that this might not scale gracefully. This was designed for a single guild with what I would call a slow chat input. How this will handle even a dozen guilds with mild to moderate chat activity is beyond my testing ability at this time.

---

#### Direct Message Commands:

*Open to anyone who can interact with the bot*

**sb!list**

- Lists stored searches for the users from all guilds in the config
- If the guildname is "Unknown" it is a guild the bot was registered in but has, since, been removed. The config stores guild IDs and we're doing a lookup to get the actual name here.

**sb!help**

- A short version of this document

**sb!on**

- Turns ShoulderBird on for *all* guilds a user has set a search in

**sb!off**

- Turns ShoulderBird off for *all* guilds a user has set a search in

**sb!set** [guild name or ID] = [Regex search]

- Sets a search (called a bird in the code) for the given guild. The guild can be the guild's name (case sensitive) or the guild's ID.
- To get the guild's ID you must have dev options on in Discord found in Options > Appearance > Developer Mode.  You can then right-click guilds, users, channels, and more to get their unique ID.
- If no [Regex search] is provided then this will be "" and ignored when searches are run.

**sb!ignore** [user name or ID]

- Toggles a user to be ignored by Shoulderbird across all guilds the user has a search in. If the target user is already on the ignore list they will be removed, otherwise they are added.
- User name is not the user's nickname and excludes the #0000 postfix.

**sb!delete**

- Deletes all of the searches in all guilds of the user. This has no confirmation and has no undo.

---

## Okay, but how does the Regex part work?

Shoulder Bird scans incoming messages and uses a custom regex expression which is word-bound at the beginning and the end. This is the base regex expression:

```python
findRg = re.compile(r'\b{}\b'.format(rx), re.I)
```

If your nickname in a chat is, for example, "Egg" and you want to be pinged when anyone says your nickname then you can start with a basic regex search:

```
sb!set MyGuild_Name = (egg)
```

*Keep in mind that we are removing case sensitivity so keep your searches lowercase for expected results.*

You can get as complex with regex as you like. There are many tools out there to help you build an expression that matches everything you want.

---

## Adding Shoulder Bird to your Discord.py bot

While created for my own egg_bot system, this module is designed to be added to any Discord bot code that is running off the discord.py library. The class needs to be initialized and then you simply pass the discord.message to the .onMessage() method.

Installation (assumes you have installed python3+ and discord.py):

[Download shoulderBird.py into your working directory](https://github.com/Preocts/Egg_Bot/blob/source/modules/shoulderBird.py)

Sample Code:
```python
import discord
import shoulderBird

client = discord.Client()
bird = shoulderBird.shoulderBird('./wherever/youwant.json')


@client.event
async def 1on_message(message):
    await bird.onMessage(message=message)

if __name__ == '__main__':
    discord_token = 'Your Secret Here'
    client.run(discord_token)
```

The first time you run this you will seen an error in the logs for a bad/missing configuration. The script is designed to fail gracefully and create everything it needs to run for the guild owner. You will need to set a search up for this to work with sb!set command in a DM to the bot.

The default config path is ./config/shoulderBird.json from your working directory.
