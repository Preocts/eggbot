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

## [Unreleased]

## [0.7.0] - 2020-11-24

### Removed

- Extra logging module that hopelessly complicated the logging process
- ./utils/eggUtils.py - There are better ways than what was being done

### Added

- Default logging setup in eggbot.py to simplify the logging process
- ./utils/modulehelper.py
  - loadjson() and savejson() to assist with configs in modules
  - EggModuleException() class for raising exceptions in the modules

### Changed

- Makefile adjustments for dependencies, clean, and new pacakge
- Basic Commands module (./modules/basicCommands.py)
  - If the config file cannot be loaded or is invalid, the module does not load
  - If the config file is blank or missing a new template is created

## [Released]