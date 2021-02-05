# -*- coding: utf-8 -*-
""" Egg Bot, Discord Modular Bot

Author  : Preocts, preocts@preocts.com
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/Egg_Bot
"""

import os
import sys
import json
import logging
import importlib

import discord


logger = logging.getLogger(__name__)  # Create module level logger


DISCORD_API = None
BOT_OWNER = None
VERSION = None
VERSION_NAME = None
LOGLEVEL = None

# Global List of Classes from modules
bot_classes = []
intents = discord.Intents.default()
intents.members = True
dClient = discord.Client(
    status="online",
    activity=discord.Activity(type=2, name="everything."),
    intents=intents,
)


# ON READY - connection established
@dClient.event
async def on_ready():
    logger.info("Egg hatched! Connection Established!")
    logger.info("Egg successfully hatched.")
    logger.info("Connection to Discord Established.")
    # logger.info('Available Guilds:')
    # for guild in dClient.guilds:
    #     logger.info(f'\t{guild}')
    return True


# ON DISCONNECT - connection closed or lost
@dClient.event
async def on_disconnect():
    logger.info("Egg Dropped. Connection lost or reset by host")
    return


# ON JOIN - Welcome the new user
@dClient.event
async def on_member_join(member):
    """ Handle the event of a user joining the guild """

    global bot_classes
    logger.info(
        f"Member Join: Display Name: {member.display_name}"
        f" | User ID: {member.id}"
        f" | Account Created: {member.created_at}"
        f" | Guild: {member.guild.name}"
    )

    for mods in bot_classes:
        try:
            await mods.onJoin(member=member)
        except AttributeError:
            continue
    return


# ON TYPING - things and stuff
@dClient.event
async def on_typing(channel, user, when):
    global bot_classes
    for mods in bot_classes:
        try:
            # I REALLY do not want to pass dClient here....
            await mods.onTyping(channel=channel, user=user, when=when)
        except AttributeError:
            continue
    return


# ON MESSAGE - Bot Commands
@dClient.event
async def on_message(message):
    """ Event triggers on every new message bot can see """

    global bot_classes
    # Ignore messages by bot account
    if message.author == dClient.user:
        return False

    if str(type(message.channel)) == "<class 'discord.channel.TextChannel'>":
        channelType = "text"
    elif str(type(message.channel)) == "<class 'discord.channel.DMChannel'>":
        channelType = "dm"
    else:
        channelType = "group"
        # Bot does not currently support Group private chats
        return False

    # SYSTEM LEVEL COMMANDS
    if str(message.author.id) == BOT_OWNER:
        # Pulse check
        if message.clean_content == "egg!bot":
            await message.channel.send(
                f"Egg_Bot version: {VERSION} - " f" {VERSION_NAME} - :egg:"
            )
            return False
        # Disconnect - System command
        if message.clean_content == "egg!disconnect":
            dropClasses()  # Save and drop our classes
            if channelType == "text":
                await message.delete()
            await dClient.close()
            return False
        # Reload Configurations - System command
        if message.clean_content == "egg!reloadAll":
            reloadClasses()
            return False
        # if message.clean_content == "egg!testjoin":
        #     await on_member_join(dClient.get_guild(621085335979294740).get_member(int(BOT_OWNER)))  # noqa: E501

    for mods in bot_classes:
        try:
            await mods.onMessage(
                chtype=channelType, message=message, client=dClient
            )
        except AttributeError:
            continue
    return


def loadCore() -> None:
    """ Loads eggbot.json from config files, set globals """
    inputFile = eggUtils.abs_path(__file__) + "/config/eggbot.json"
    with open(inputFile) as file:
        try:
            configs = json.load(file)
        except json.decoder.JSONDecodeError:
            logger.critical(
                "Configuration file empty or formatted "
                "incorrectly, that's sad"
            )
            exit()
        except OSError:
            logger.critical("Something went wrong loading configuations...")
            logger.critical("", exc_info=True)
            exit()
    global VERSION
    VERSION = configs["CoreConfig"]["Version"]
    global VERSION_NAME
    VERSION_NAME = configs["CoreConfig"]["VersionName"]
    global LOGLEVEL
    LOGLEVEL = configs["CoreConfig"]["Debug_Level"]
    global DISCORD_API
    DISCORD_API = configs["discord_api_key"]
    global BOT_OWNER
    BOT_OWNER = configs["owner"]
    return


def find_modules() -> tuple:
    """ Searches the ./modules directory for loadable modules """
    module_list = []
    mypath = eggUtils.abs_path(__file__) + "/modules"
    for file in os.listdir(mypath):
        if file.endswith(".py") and not (file.startswith("__")):
            importlib.import_module("eggbot.modules." + file[:-3])
            module_list.append(file[:-3])
    return tuple(module_list)


def load_classes(module_list: tuple):
    """Handles the classes for the bot

    This should only be run if no classes are initialized. Otherwise, This
    will create duplicate instances which will lead to unexpected behavior.
    """
    global bot_classes
    count = 0

    for mod in module_list:
        try:
            logger.info(f"Loading initClass() for: {mod}...")
            bot_classes.append(
                sys.modules["eggbot.modules." + mod].initClass()
            )  # noqa
            logger.info(f"Successfully loaded initClass() for: {mod}")
        except AttributeError:
            logger.info(f"No initClass() found for: {mod}")
        count += 1

    logger.info(f"Loaded {count} modules for Egg_Bot")
    return


def reloadClasses():
    """ Reload classes that allow a forced reload """
    global bot_classes
    for mod in bot_classes:
        try:
            if mod.allowReload:
                mod.loadConfig(mod.activeConfig)
        except AttributeError:
            continue
    return


def dropClasses():
    """ Drops (destroys) all class instances. """
    global bot_classes
    for x in range(0, len(bot_classes)):
        bot_classes[x] = None
    return


def main() -> None:
    """Main Point of Entry

    Any setup, configuration, or async setups must happen before the main
    run loop prior to the exit.
    """
    logger.info("Loading config...")

    loadCore()

    c_file = eggUtils.abs_path(__file__) + "/config/logging_config.json"
    logging_init.config_logger(c_file, LOGLEVEL)
    logger.info("Config loaded, assets contained, plans are hatching...")
    logger.info("Checking for any extra modules...")
    module_list = find_modules()
    logger.info(f"Found {len(module_list)} in the fridge behind the milk.")
    logger.info("Cracking the module carton open for more supplies...")
    load_classes(module_list)
    logger.info("Loaded yolk configuration file.")
    logger.info(f"Eggbot version: {VERSION}")
    logger.info(f"Eggbot version name: {VERSION_NAME}")
    logger.info(f"Logging level: {LOGLEVEL}")
    logger.info("Hatch cycle started...")
    logger.info("Hatching onto Discord now.")
    dClient.run(DISCORD_API)
    dropClasses()
    return


if __name__ == "__main__":
    main()

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
