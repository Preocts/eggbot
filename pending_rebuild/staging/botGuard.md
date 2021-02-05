# Bot Guard Module v1.0.0

### Kicking bots that aren't invited. Why? Because.

Bot Guard scans for joining bots and, if they are not on the allow list in the config, it will kick them from the guild.

This does require the bot running this module to have permissions to kick members.

Only the guild owner can control this module as-is. This is intentional as only administrators and managers can invite bots. If you need this module there is no need to put it in the hands of anyone else.

**This only watches for new joins. Bots already in the guild will not be impacted unless they rejoin**

---

#### Chat Commands:

*Run in any channel the bot is active in. Configuration applies to the guild the command is run in*

**guard!help**

- Display a shortened version of this document in the chat the command is run.

**guard!on**

- Turn the Bot Guard module on. Default on install to a new guild is **off**.

**guard!off**

- Turn the Bot Guard module on. Default on install to a new guild is **off**.

**guard!allow** [memberID]

- Adds a bot ID to the allow-list which will stop Bot Guard from kicking that bot on join.
- If already listed the ID will be removed.
- To find the memberID you need to enable Developer Mode in Discord.
  - Open User settings (the gear)
  - Click "Appearance"
  - Scroll down and select "Developer Mode" in the Advanced section
  - You can now right-click users/channels/guilds and "Copy ID"

**guard!channel** [#Channel_Mention]

- Any actions Bot Guard takes will be announced. Set the channel these actions are announced with this command.
- Not including a #Channel_Mention will clear the set channel.
- When no channel is set, Bot Guard will DM the guild owner.

**guard!fail** [message]

- Customize the announcement when a bot joins that was not on the allow list.
- Use the placeholder "{id}" to get the bot ID in the custom message.

**guard!pass** [message]

- Customize the announcement when a bot joins that was on the allow list.
- Use the placeholder "{id}" to get the bot ID in the custom message.

---

## Adding Bot Guard to your Discord.py bot

While created for my own egg_bot system, this module is designed to be added to any Discord bot code that is running off the discord.py library. The class needs to be initialized and then you simply pass the discord.message to the .onMessage() method.

Installation (assumes you have installed python3+ and discord.py):

[Download shoulderBird.py into your working directory](https://github.com/Preocts/Egg_Bot/blob/source/modules/shoulderBird.py)

Sample Code:
```python
import discord
import botGuard

client = discord.Client()
guard = botGuard.botGuard('./wherever/youwant.json')


@client.event
async def on_message(message):
    await guard.onMessage(message=message)

@client.event
async def on_member_join(member):
    await guard.onJoin(member=member)


if __name__ == '__main__':
    discord_token = 'Your Secret Here'
    client.run(discord_token)
```

The first time you run this you will seen an error in the logs for a bad/missing configuration. The script is designed to fail gracefully and create everything it needs to run for the guild owner.

The default config path is ./config/botGuard.json from your working directory.

**The default state of this new config is disabled.**
