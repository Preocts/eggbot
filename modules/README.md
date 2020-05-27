# Egg Bot Module Documentation

## ShoulderBird - RegEx message alerting

###### shoulderBird.py

---

ShoulderBird is a module that uses RegEx to scan incoming message events. If a match is found for a specific user on a specific server then that user can be alerted by a bot. **Note**: Creates, updates, and deletes to the loaded configuration file do not save to disk. A call to save **must** be made independently prior to the class being unloaded.

**RegEx searches are case insensitive**

Created by Preocts

[preocts@preocts.com](mailto:preocts@preocts.com) | Preocts#8196 Discord | [Github](https://github.com/Preocts/Egg_Bot)

#### Common Use Examples:

Initialize: (loads config file)
```python
SB = shoulderBird.shoulderBird("FileNameOptional")
# FileName will load given json config
# Defaults to ./config/shoulderBird.json
```

Create/Update a search:
```python
results = SB.putBird("GuildName", "UserName", "RegEx Search String")
```

Delete a search:
```python
results = SB.delBird("GuildName", "UserName")
```

Toggle a search on/off (returns new state):
```python
results = SB.toggleBird("GuildName", "UserName")
```

Scan a message for a matching search:
```python
results = SB.birdCall("GuildName", "UserName", "Message String")
# If results["status"] is True then results["response"] will be
# the username of who had a matching search.
```

Save Config:
```python
SB.saveConfig("FileNameOptional")
# Defaults to ./config/shoulderBird.json
```

#### Returns

In most cases all returned values a dictionary with the following format:

*Pass/True*
```json
{ "status": true,
  "response": "Expected response" }
```

*Fail/False*
```json
{ "status": false,
  "response": "Fail reason" }
```

Configuration file example:
```json
{
    "GuildName": {
        "Preocts": {
            "regex": "(pre(|oct|octs)|oct(|s)|egg)",
            "toggle": true
        },
        "DifferentUser": {
            "regex": "(raffle|contest|free|give(|away|-away))",
            "toggle": false
        }
    },
    "Different GuildName": {}
}
```

---

## Join Actions - Bot actions on new member join

###### joinActions.py
---

These are special actions that happen when a member joins a guild. For now they are limited to welcome messages sent to chats or to DMs. Future scope of this module is to allow for custom role assignments based on invite codes, exclusive messages for roles, and exclusive messages for invites.

Created by Preocts

[preocts@preocts.com](mailto:preocts@preocts.com) | Preocts#8196 Discord | [Github](https://github.com/Preocts/Egg_Bot)

#### Common Use Examples:

**Initialize: (loads config file)**
```python
SB = joinActions.joinActions("FileNameOptional")
# FileName will load given json config
# Defaults to ./config/joinActions.json
```

**Create a joinAction:**
```python
results = SB.create("GuildName", **kwargs)
```
Keyword Args:
- name: Unique name for the join action **Required**
- channel: Channel any message is displayed.
  - Leaving this blank will result in a direct message
- addRole: Grants user a list of roles on join **Inactive**
- message: Displays this message to given channel/DM
- active: Boolean toggle
- limitRole: List roles required to recieve this join action **Inactive**
- limitInvite: List invite IDs required to recieve this join action **Inactive**

**Read existing joinAction:**
```python
results = SB.read("GuildName", "ActionName")
```

**Read all joinActions from a Guild:**
```python
results = SB.readAll("GuildName")
```

**Update existing joinAction:**
```python
results = SB.update("GuildName", "ActionName", **kwargs)
```
*See Create a joinAction for keyword args*

**Delete existing joinAction:**
```python
results = SB.update("GuildName", "ActionName")
```

**Load Config:**
```python
SB.loadConfig("FileNameOptional")
# Defaults to ./config/joinActions.json
```

**Save Config:**
```python
SB.saveConfig("FileNameOptional")
# Defaults to ./config/joinActions.json
```

#### Returns

In most cases all returned values a dictionary with the following format:

*Pass/True*
```json
{ "status": true,
  "response": "Expected response" }
```

*Fail/False*
```json
{ "status": false,
  "response": "Fail reason" }
```

**Configuration file example:**
```json
{
    "GuildName": [
        {
            "name": "Welcome_Chat",
            "channel": "General-chat",
            "roles": "",
            "message": "This will be displayed in the chat",
            "active": true,
            "limitRole": "",
            "limitInvite": ""
        },
        {
            "name": "Welcome_DM",
            "channel": "",
            "roles": "",
            "message": "Because this has no channel, it will be a DM",
            "active": true,
            "limitRole": "",
            "limitInvite": ""
        }
    ]
}
```

---

## Basic Commands - Bot chat interaction made complex!

###### basicCommands.py
---

This module focuses on what is called a "Basic Command" or a command that does not execute any code and is only expected to return a message for display in chat or DM.

Commands are VERY controllable on who can run them, where, and how often. Whether by broad channel or user exclusions or specific user/role/channel inclusion, this module will handle it all. Or, just leave the commands open to be run whenever by whomever. Let chaos run wild, pantless, and free!

Created by Preocts

[preocts@preocts.com](mailto:preocts@preocts.com) | Preocts#8196 Discord | [Github](https://github.com/Preocts/Egg_Bot)

#### Common Use Examples:

**More documentation coming in future versions.  Manual configuration editing is needed as of v0.3.1 with no system commands available**

```json
{
    "GuildName": {
        "prohibitedChannels": ["ChannelName", "OtherChannel"],
        "prohibitedUsers": ["ThisGuyNeverRunsCommands"],
        "guildCommands": {
            "!command": {
                "users": ["OnlyICanRunThisCommand"],
                "channels": ["OnlyInThisChannel", "AndThisOne"],
                "roles": [],
                "throttle": 10,
                "lastran": 0,
                "content": "This will be the output!",
                "help": "What will this do?"
            }
        }
    }
}
```
