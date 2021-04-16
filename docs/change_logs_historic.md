# This log was retired on 2020.11.24

# New log is found here: [CHANGELOG.md](CHANGELOG.md)

##### Change Log v0.6.9 - Fickled Egg - Bot Guard v1.0.0

- Bot Guard gets a redesign and updated to a full release version
- [x] Load config or create new
- [x] Save config and create new file/path
- [x] Check if config has guild (build defaults if needed)
- [x] Active toggle
- [x] Control commands
  - [x] Guild owner access only
  - [x] guard!help : Display help
  - [x] guard!on : Turn gaurd on
  - [x] guard!off : Turn guard off
  - [x] guard!allow [member id] : Add/Remove provided ID
  - [x] guard!channel [#channel] : Set sqwuak channel
  - [x] guard!fail [messge] : Set denied entry message
  - [x] guard!pass [message] : Set allowed entry message
- [x] onJoin action
  - [x] Check if joining member is a bot (discord.member.bot)
  - If bot:
    - [x] Kick if discord.member.id not on allow list
    - [x] Announce action in announce_channel of config
    - [x] If channel is not set, DM guild owner


##### Change Log v0.6.8 - Fickled Egg - ShoulderBird v1.0.0

- ShoulderBird gets a refactor and updated to a full release version
- [x] Update load/save to be standalone (remove json_io)
- [x] Remove eggUtil dependency
- [x] Clean up Docstrings
- [x] Config Health Check
- [x] Streamline commands
  - [x] sb!on
  - [x] sb!off
  - [x] sb!ignore [name#0000/id]
  - [x] sb!set [guild name/id] = [regex]
  - [x] sb!list
  - [x] sb!delete
  - [x] sb!help

##### Change Log v0.6.7 - Fickled Egg - Kudos and tweaks

- Adjusted some internal formatting of modules
- Released Chat Kudos v1.0.0
  - https://github.com/Preocts/Egg_Bot/blob/source/docs/chatKudos.md


##### Change Log v0.6.6 - Fickled Egg - Patch of Patch

- Fixed display_name issue with Kudos. Was pulling a user object from client level instead of a member object from guild level. This caused them to not have a nickname.
- Fixed a variable name re-use that was causing user names, not IDs, to be logged. Did not impact run-time.
- **Space is required** between the @mention and the +s or -s.
- Side-effect of this: "@preocts +-Hello-World++" is now a completely valid way to grant 1 point.
  - Yes, this means that "++O--w--O++" looks fun, and does nothing in regards to points.

##### Change Log v0.6.5 - Fickled Egg - Patch

- Fixed a dozen bugs with Kudos module. Thanks Nay for field testing
- Added missing changelog for 0.6.4 (it was a late night, okay?)
- Kudo module will need user IDs filled into {"controls": "users": [] } list to be functional at this time
- Future release will include permissions based on channel, role, and user
- Future release will include chat driven control commands for changing this settings


##### Change Log v0.6.4 - Fickled Egg - Kudos

- chatKudos module : points to users for your own amusement and chaos
  - @username++++ : adds four points
  - @username---- : removes four points
  - The number of + or - immediately following a mention is the number of points granted or removed
  - kudo!board (N)
    - Display top 10 point holders (default)
    - Optional: provide N for specific number of results


##### Change Log v0.6.3 - Fickled Egg - Chat commands

- basicCommands changes/additions:
  - command!add [commandname] [command text]
    - Adds a command to the guild
    - Used in guild chat only
  - command!mod [commandname] [-/+/-+] [flag] [value]
    - modifies flags for a command
      - "-" remove or subtract
      - "+" append or add
      - "-+" replace completely
    - Valid flags are currently
      - users : Limit use of command to only these IDs
      - channels: Limit use of command to only these channel IDs
      - roles: Limit use of command to only these role IDs
      - cooldown: Define how many seconds between each run of this command
      - text: Define what the command returns to chat
      - help: Not currently used
  - command!del [commandname]
    - Permanently deletes a command

---

##### Change Log v0.6.2 - Fickled Egg

- typingReact changes/addition:
  - Added check for guilds that are opted out of this feature
  - Should now react to channel specific counts of users typing within a 9 second window
  - Removed a bug that had multiple channels counting toward the same goal
- Logging calls updated to be more uniform across all modules
  - Log files are now:
    - full_logs.log - All run-times, 10mb max, 5 file rotation
    - single_logs.log - Single run-time, volatile file
    - console logging is on by default
- Moved jsonIO.py to ./utils as it is nothing but helper functions
- Moved logging_init.py to ./utils as it is a helper function

---

##### Change Log v0.6.1 - Fickled Egg

**This feature change is not backward compatible**

- README - Spelling corrections
- shoulderBird - toggleBird() - bug fix: possible to return undefined variable
- shoulderBird - Formatting corrections
- shoulderBird - Changed dm output to use .join instead of "+" because it's more efficient.
- basicCommands - Refactor:
  - addCommand() now just does simple commands to keep it simple
    - expected input: "command!add [commandname] [command text]"
  - modCommand() created to handle modifying commands
    - expected input: "command!mod [commandname] [(+/-/-+)key] [input]
    - "+": append(add), "-": remove(lists only), "-+": replace all
    - example: "command!mod !myCommand +roles Mods, VIPs"
      - Adds "Mods" and "VIPs" to roles list
- typingReact.py created and prototyped
  - Events and such for when people are typing. Don't know where this one is going.
  - Current default includes reactions at 5, 10, 15, and 20 people typing with a 3 second window
  - Each level of escalated #s has its own cooldown
  - Default cooldown is 24 hours
- Updated ALL hooks in modules to only take keywords args. Saving headaches one day at a time.

---

##### Change Log v0.5.2 - Opus Egg

- Added chtype to the OnMessage class method call in egg_bot.py
  - chtype (str) : Channel Type: text, dm, or group
- Added \*\*kwargs to class methods for future growth
  - Also allows passing the discord instance which is helpful
- General DM "!help" command implemented
  - Will step through all available "general" help commands in each module. Used to offer a more specific guide from loaded modules.
- ShoulderBird DM commands now functional.
  - sb!help
    - Displays this list
  - sb!set [guild name/ID] = [RegEx]
    - Sets a user's RegEx search for given guild
  - sb!toggle [guild name/ID]
    - Toggles a search without deleting it
  - sb!ignore [guild name/ID] = [name/ID]
    - Toggle a specific user to be ignored by ShoulderBird
  - sb!remove [guild name/ID]
    - Deletes a stored search from given guild
  - sb!list [guild name/ID]
    - Lists stored search from given guild
- eggUtils.py - simple helper function storage

---

##### Change Log v0.5.1 - Opus Egg

- Modules in the ./module path are now dynamically loaded
- What does this mean?
  - I can't forget to update the \_\_init\_\_.py again
  - Module classes are instanced from a standard modules.moduleName.initClass() function
  - Classes are loaded into a list of objects
  - Classes are iterated through during events with a call to a standard method. (onJoin, onMessage)
  - If the method doesn't exist, the script moves on gracefully (no errors, no logs)
  - As new modules are created, following the template, they can be dropped into the directory and will just "work"
- Fixed a poor copy/pasta that was causing guildMetrics to save in basicCommands.json.
- Module specific changes:
  - Classes for modules now have a class variables:
    - instCount (int): Count of active instances of class
    - name (str): Name of class
    - allowReload (bool): Allow/deny the class to reload config from file without saving
- Core script changes:
  - No code handling module responses remains, completely migrated into modules.

---

##### Change Log v0.4.2 - Annul Egg
- Logging tweak to reduce the number of handlers and simplify my life.
- Some core level tweaks to ensure required directories exist
- Documentation updates

---

##### Change Log v0.4.1 - Annul Egg
**This feature change is not backward compatible**
- Configuration files now use guild IDs instead of names
- Configuration files now use user IDs instead of names
- Configuration files now use channel IDs instead of names
- Configuration files now use role IDs instead of names
- Catching a trend?
- json_io.py saveConfig() has a new optional argument
  - raw=False : (default) Readable JSON with an indent of 4 spaces
  - raw=True : No formatting to the config will be applied
- New module: guildMetrics.py
  - Tracks harmless metrics of a guild
    - Guild names by ID (history)
    - Member names by ID (history)
    - Member nicknames by ID (history)
    - "First seen" and "Last seen" for members
    - Message counters:
      - Number of total messages sent
      - Number of words sent (by space delimit)
      - Number of messages that ended with a period "."
    - Hours - 24 hour breakdown of activity
      - Okay, this one blurs the line of creepy. I admit it.
- New module: botGuard.py
  - Will do nothing for now unless configured manually
  - Auto-kicks new bot joins unless the bot is on the Allow-list.
    - Spam/Malicious protection

---

##### Change Log v0.3.5 - shoulderBird enhancements
- Logging adjustments in modules. Shifted to mostly all debug level for noise reduction.
- guildMetrics module created
  - Tracks generally useless metrics of guilds and members
  - "In trial" - no promise this makes it to v1

---

##### Change Log v0.3.4 - shoulderBird enhancements
- Bug fix: No need to check username in bird search. It resulted in all negative searches unless the person typing was the person the shoulderBird ping was for which... defeats the purpose.  Honestly angry at this mistake I made.
- Bug fix: anti-snoop was looking at the wrong name. Again, the user typing the message can be assumed to be in the room the message is typed. Just sayin'
- Bug fix/Enhancement: Return a list of birds(users) found instead of finding first regex match and returning.

---

##### Change Log v0.3.3 - basicCommands enhancements
- addCommand method created. Supports simple or complex commands
  - Simple Command:
    - !setTrigger !command Whatever the command will say in chat
  - Complex Command:
    - !setTrigger !command | content = Whatever the command will say | roles = RoleRestriction | users = UserName
  - Key list: users, channels, roles, throttle, content, help
- ShoulderBird can now ignore specific users on specific guilds
- ShoulderBird will no longer chirp if the user isn't in the room a message is seen in.
- Fixed issue with owner command trying to delete a DM message

---

##### Change Log v0.3.2 - Clean-up
- __str__ output format of joinActions.py changed (removed json.dumps)
  - Same done for basicCommands.py
  - Same done for shoulderBird.py
- Import of json removed from joinActions.py, basicCommands.py, shoulderBird.py
- saveConfig and loadConfig methods adjusted to call from json_io module (for unified file input/output)
  - Done in shoulderBird.py and joinActions.py
- Migrated the rest of joinAction code not dealing with discord objects to the module
  - Created getJoinMessage() method to process on_member_join events
- Added error checks for empty joinAction messages

---

##### Change Log 0.3.1 - Refactor I
- Created Module for ShoulderBird
- New config file for ShoulderBird
- Load and Save config file for ShoulderBird created
- Directory restructure including new folders:
    + config : all configuration files
    + logs : all log outputs
    + modules : all module code
- Python Logging Added
- Logger configuration and init code completed

- Created Module for joinActions
    + Better welcome message configuration methods!
    + Set roles on join
    + Future update: roles for specific invites!

- Standard output format for methods
- Small changes to eggbot.py
    + Very tiny
    + You wouldn't notice at all
    + Also not backward compatible, at all

- json_io helper scripts created to ease loading/saving json configs
    + Custom Raise Class: JSON_Config_Error
- Created Module for basicCommands
    + VASTLY definable restrictions
    + Throttle to prevent spam
    + basicCommands only return a value to print to a channel

---

##### Change Log 0.2.8 - patch
- Removed optout references for the time being

---

##### Change Log 0.2.7 - ShoulderBird patch
- Fixed the regEx search to include proper word boundaries
- Secret command actions for funs

---

##### Change Log 0.2.6 - ShoulderBird patch
- ShoulderBird now uses message.clean_content for better output. (remove @123456789 with mentions)

---

##### Change Log 0.2.5 - Opt-Out Options
- Hotfix: missed 'await' in on_member_join updates. I am full of cocoa
- Hotfix: discord.member class behaving weirdly in on_member_join - rolled back to the old code (kinda)
- EggConfig additions
    + optoutFlag = {'UserID': 'Boolean'}
    + def optoutToggle(discord.member.id)
- New DM command actions
    + optout-toggle : Toggles the optout flag for any given user.
- New config key {optoutToggle} : stores boolean flags against discord.member.id
    + Added config load to eggConfigFile.loadConfig() and eggConfigFile.saveConfig()
- on_member_join now checks for optoutToggle status

---

##### Change Log 0.2.4 - Hotfix
- Corrected sb-set action so that it no longer removes all one entry in ShoulderBird searches

---

##### Change Log 0.2.3 - ShoulderBird
- Formatting changes.
- on_member_join updated to use the proper DM and Chat calls
    + It was previously using its' own call, how arrogant
    + Also removed image support - this was only half-baked at best
- Removed check for empty guildname input for command methods. We're using an empty guild for DM Commands
- ShoulderBird method created: toggleBird {username}
- ShoulderBird specific commands created:
    + sb-toggle : Toggle ShoulderBird on and off
    + sb-set {guildname} = {regEx}: Replace existing (or create) regEx ShoulderBird search
    + sb-show : Output current regEx ShoulderBird search for all guilds
    + sb-delete {guildname} : Delete search from provided guild

---

##### Change Log 0.2.2
- tore apart (refactored) on_message
    + Shoulder Bird gets its own def
    + Commands go to their own def
    + Chat messages and DM message briefly had their own def
    + Handles Chat and DM messages differently
- "botCommands" section added to json config
    + botCommands{} -> GuildName{} -> CommandName{} -> CommandConfigs{}
- created handler_ChatMessage and handler_DMMessage
- deleted handler_ChatMessage and handler_DMMessage
- Questioned my sanity
- Class additions
    + botCommands dict
    + listCommand(GuildName) - returns list of command names set in Guild
    + getCommand(GuildName, CommandName) - returns dict of specific command
    + putCommand(GuildName, FullChatLine)
        - sets command, does all the parsing needed (send discord.py message.content)
        - will override existing commands - allows for update/editing easier
        - e!command [commandname] < | option = option value | option2 = option2 value >
    + delCommand(GuildName, CommandName) - deletes given command
- TWO MONTHS LATER
- Completely refactored on_message def, again.  This time it's solid (er)
    - Missing shoulder bird call
- Command actions defined:
    + 'edit-command' : used for create/edit of commands
    + 'show-command' : used to return the same string used to config a command
    + 'delete-command' : used to delete a command from the guild/DM
    + 'list-command' : used to return a list of all commands in guild/DM
- Class updates:
    + 'getBird' : returns a specific user's ShoulderBird search
    + 'getBirds' : returns a guild's dict of ShoulderBird searches
    + 'putBird' : create/update a user's search (adds guild if missing)
    + 'delBird' : deletes a user's entry.  Why would you do this?
- Command permissions (users/channels/roles) now work
- No way to remove a permission once set, this will be backlogged
    + Work-around now is to delete the command and recreate it
- Command have no guardrails. You can delete the only command allowing edits/creates
    + No work-around. Backlogged for enhancements
- Updated base.egg to show some default commands
- Updated README.md - the struggle is real

---

##### Change Log 0.2.1
- Input parameter for configuration file created.
    + egg_bot.py <filename>
    + if parameter is not provided default is 'base.egg'
- More verbose console output on launch
- More egg references
- logOutput now takes a fileName argument - future scope work
- Updates to eggConfig class
    + addGuild created
- on_chat_message upgrades
    + Separate handlers for DM chats
- Tweaked many str(message.guild) to just message.guild.name since that makes more sense
- sendChatMessage now only sends messages to chat rooms
- sendDMMessage created to handle all DM traffic
- Config file refactor
    + using JSON now to store configs
    + implemented configs: Guild Configs, Shoulder Bird
    + planned configs: Sass Back, Custom !commands, Opt-Out List
- Class changes
    + addGuild removed (didn't last long)
    + Refactor to use JSON
    + addConfig parameter change
- Code Changes:
    + instances of .addGuild changed to .addConfig

---

##### Change Log 0.1.3
- renamed class eggINI to eggConfig
    - renamed dict iniFile to configFile
- removed def loadFile() from code
- Updates to eggConfig class
    + loadConfig, saveConfig, listConfig, listActiveFile, listConfigFiles : created
    + Smarter return values for error handling
- Bot now attempts to load 'base.egg' and fails if not found
- Known bug - Bots don't like greeting other bots (sending DMs)
- Known bug - setting an image file for greetings and not having the image causes an ungraceful exception

---

##### Change Log 0.1.2
- Added support for Keyword to config file
    + [MENTION] - @ tag of user display name
- Added config line "allowedChatRooms"
- Bot will only listen and response in "allowedChatRooms" on server
- Added config line "autowelcomeChannel"
- Bot will only post guild level welcome announcements to "autowelcomeChannel"
- 'eggbot', 'greetme', 'disconnect' are now Owner Only commands
- Added more verbose command logging
- Added to eggINI Class
    + isAllowedChat
- ShoulderBird moved to its own routine (also now called ShoulderBird)
- Removed FindNay (replaced with ShoulderBird)
- Hard coded use for ShoulderBird (Future INI planned)
- on_message now conditions according to the channel type (Chat/DM/Group)

---

##### Change Log 0.1.1
- Logging for connection added
- Logging for disconnect added
- Removed event for status changes
- On Join event added
- Output standard for egg.log created
- Logging for commands
- Logging for new joins
- Added Support for keys to config file
    + @, names the guild following keys are applied to
    + &, configuration settings
- Added support for Keywords to config file
    + [USERNAME] - user's display name (nickname if set)
    + [GUILDNAME] - Guild name
- Nay finder added *specifically requested feature
- Logging for commands actually added
- Baked commands now only answer to OWNER
- env control for bot's owner added
- !greetme command to get the bot greetings without leaving/joining
- eggINI class
    + addConfig, getConfig, hasGuild, hasMember, getMember, addMember
