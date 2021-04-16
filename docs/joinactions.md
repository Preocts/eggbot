# JoinActions module

Offers a simple configuration driven event handler for when a member joins a Discord guild. With room to expand, this offer a great starter module. Schedule a viewing before it is gone!

JoinActions trigger **immediately** on delivery of the join event and execute as quickly as possible.

**NOTE**: This module currently requires manual editing of the config file
for setup.

**TO DO**:
- CLI controls
- Assign role(s) on join
- Evaluate invite id on join

---

### Config schema

```json
{
    "module": "JoinActions",
    "version": "1.0.0",
    "[GUILD ID]": [
        {
            "name": "[UNIQUE ACTION NAME]",
            "channel": "[CHANNEL ID | EMPTY STRING FOR DM",
            "message": "[MESSAGE TO SEND TO CHANNEL OR DM]",
            "active": true,
        },
        ...
    ]
}
```

A single guild entry holds an array of actions to take.

- `module` : No implemented use
- `version` : No implemented use
- `[GUILD ID]` : String value of the guild ID where actions will be executed
  - `name` : A unique name of the action for future implementation
  - `channel` : String value of the channel ID the message will be displayed in
    - If left empty (`""`) a direct message to the joining use will be attempted instead
  - `message` : Full message to present on join. Some metadata tags are supported, see below
  - `active` : Boolean value, if `false` the action will not be executed

---

### Metadata values

There are some Metadata values you can place in the `message` which will be replaced on use of the string. To use, ensure the entire tag is entered as shown below. This **includes** the surrounding square-brackets.

| Metadata tag | Description |
|--|--|
| `[GUILDNAME]` | Name of the guild where the join even happened |
| `[USERNAME]` | Username of the member joining the guild |
| `[MENTION]` | Same as Username only will trigger an @ mention |
