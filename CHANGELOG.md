# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

## [0.0.8-alpha] - 2021.04.18

### Added
- ChatKudos refactor completed:
  - `chatkudos` module updated
  - Documentation completed
  - Testing completed
- ChatKudos loaded into event system (on message)

### Changed
- ShoulderBird will send `clean_content` of the message to make mentions readable

## [0.0.7-alpha] - 2021.04.17

### Added
- JoinAction refactor completed:
  - `joinactions` reduced to only live code
  - Documentation completed
  - Testing completed
- JoinActions loaded into event system

### Changed
- Typing hinting for event_sub `CALLBACKEVENT`, couldn't get `protocol` to overload politely

### Removed
- Removed `error` logging lines which were glorified debug lines

## [0.0.6-alpha] - 2021.04.16

### Added
- Loading modules in `__main__.py` as a holding pattern for auto-loader
- Cleaned up a ton of calls
- ShoulderBird refactor completed:
  - `shoulderbirdconfig` holds and manages config file
  - `shoulderbirdparser` manages scanning for search keys
  - `shoulderbirdcli` allows configuration from direct message chat
  - Documentation

## [0.0.5-alpha] - 2020.11.29

### Added
- EventSub() to core_entities
- Global for EventSub() object to eggbot_core called "eventpub"
- Event function for on_member_join
- Event function for on_message

## [0.0.4-alpha] - 2020.11.28

### Added
- .cwd property to core_entities.CoreConfig()

### Changed
- Default core configuration file location moved to root of working directory
- rename: eggbot.json <---> eggbot_core.json
- Adjusted setup.py entry point to use __main__.py
- Updated `package` for Makefile to move configs in with .zip properly

### Deprecated
- .abs_path property for core_entities.CoreConfig()
  - Was referencing config files, turns out that's bad. No need for this.

## [0.0.3-alpha] - 2020.11.27

### Added
- ### eggbot_core.py
  - global `DISCORD_TOKEN` - it holds the secret loaded from environmental variable.
  - import `os`, `discord`, and `dotenv`
  - Logging output for load_config()
  - main() now exists and the bot actually connects to Discord. We're done, right?
- __main__.py for single point of entry
- Install instructions for README.md
- setup.py file for install and testing
- Makefile configurations for install, update, package, and testing
- MANIFEST.in for package data

### Changed
- Added `owner_id` to default configuration json. Future me will figure out how to populate it.
- [test] Tweaks to `test_core_entities.py` to account for above change
- [test] Corrected use of depreciated `Equals` assert
- Updated trivis.yaml for new install and testing requirements
- Corrected double // in default pathing for default configuration files

### Removed
- Removed methods `api_token` and `owner_id` from core_entities.CoreConfig class


## [0.0.2-alpha] - 2020-11-26

### Added

- eggbot_core.py, New core bot file started
  - Unit tests started, passing/incomplete

### Changed

- Structure, Directory restructure
- README, Enviromental variable references

## [0.0.1-alpha] - 2020-11-26

## [0.0.1-alpha] - 2020-11-26

## This is a rebuild change and is currently non-functional.

### Added

- core_entities.py, CoreConfig class for loading, saving, and CRUD actions on JSON configutation files.
  - Unit tests complete, passing
- ./utils/logdec.py, Log decorator for debug output
  - Logs all arguments entering a wrapped function
  - Logs returned value on exit of wrapped function
  - Unit tests completed, passing

### Changed

- egg_bot.py, completely broken with this push
- Makefile adjustments for dependencies, clean, test, and package creation

### Removed

- Everything not listed here
