# Egg Bot Module Documentation

## ShoulderBird - RegEx message alerting

---

ShoulderBird is a module that uses RegEx to scan incoming message events. If a match is found for a specific user on a specific server then that user can be alerted by a bot. **Note**: Creates, updates, and deletes to the loaded configuration file do not save to disk. A call to save **must** be made independently prior to the class being unloaded.

Created by Preocts

[preocts@preocts.com](mailto:preocts@preocts.com) | Preocts#8196 Discord | [Github](https://github.com/Preocts/Egg_Bot)

Common Use Examples:
---
Initialize: (loads config file)
```python
SB = shoulderBird.shoulderBird("FileNameOptional")
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
```
