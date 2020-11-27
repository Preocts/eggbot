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

## [0.0.2-alpha] - 2020-11-26

### Added

- eggbot_core.py, New core bot file started
  - Unit tests started, passing/incomplete

### Changed

- Structure, Directory restructure
- README, Enviromental variable references 

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
