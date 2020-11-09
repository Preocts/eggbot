"""
Egg Bot, Discord Modular Bot

Created by Preocts
    Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

"""

# Additional imports
import os
import sys
import discord
import json
import logging
import modules
import asyncio
from dotenv import load_dotenv
from eggbot.utils import logging_init

logger = logging.getLogger(__name__)  # Create module level logger

load_dotenv()
BOT_OWNER = os.getenv('BOT_OWNER')
VERSION = None
VERSION_NAME = None
LOGLEVEL = None

# Global List of Classes from modules
botMods = []
dClient = discord.Client(status='online',
                         activity=discord.Activity(type=2, name="everything."))


# ON READY - connection established
@dClient.event
async def on_ready():
    logger.info('Egg hatched! Connection Established!')
    logger.info('Egg successfully hatched.')
    logger.info('Connection to Discord Established.')
    # logger.info('Available Guilds:')
    # for guild in dClient.guilds:
    #     logger.info(f'\t{guild}')
    return True


# ON DISCONNECT - connection closed or lost
@dClient.event
async def on_disconnect():
    logger.info('Egg Dropped. Connection lost or reset by host')
    return


# ON JOIN - Welcome the new user
@dClient.event
async def on_member_join(member):
    """ Handle the event of a user joining the guild """

    global botMods
    logger.info(f'Member Join: Display Name: {member.display_name}'
                f' | User ID: {member.id}'
                f' | Account Created: {member.created_at}'
                f' | Guild: {member.guild.name}')

    for mods in botMods:
        try:
            await mods.onJoin(member=member)
        except AttributeError:
            continue
    return


# ON TYPING - things and stuff
@dClient.event
async def on_typing(channel, user, when):
    global botMods
    for mods in botMods:
        try:
            # I REALLY do not want to pass dClient here....
            await mods.onTyping(
                channel=channel,
                user=user,
                when=when)
        except AttributeError:
            continue
    return


# ON MESSAGE - Bot Commands
@dClient.event
async def on_message(message):
    """ Event triggers on every new message bot can see """

    global botMods
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
        if message.clean_content == 'egg!bot':
            await message.channel.send(f'Egg_Bot version: {VERSION} - '
                                       f' {VERSION_NAME} - :egg:')
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

    for mods in botMods:
        try:
            await mods.onMessage(
                chtype=channelType,
                message=message,
                client=dClient)
        except AttributeError:
            continue
    return


def loadCore(inputFile: str = './config/eggbot.json') -> bool:
    with open(inputFile) as file:
        try:
            configs = json.load(file)
            global VERSION
            VERSION = configs["CoreConfig"]["Version"]
            global VERSION_NAME
            VERSION_NAME = configs["CoreConfig"]["VersionName"]
            global LOGLEVEL
            LOGLEVEL = configs["CoreConfig"]["Debug_Level"]
        except json.decoder.JSONDecodeError:
            logger.critical('Configuration file empty or formatted '
                            'incorrectly, that\'s sad')
            exit()
        except OSError:
            logger.critical('Something went wrong loading configuations...')
            logger.critical('', exc_info=True)


def loadClasses():
    """
    Handles the classes for the bot

    This should only be run if no classes are initialized. Otherwise, This
    will create duplicate instances which will lead to unexpected behavior.

    Args:

    Returns:

    Raises:
    """

    global botMods

    for mod in modules.MODULE_NAMES:
        try:
            logger.info(f'Loading initClass() for: {mod}...')
            botMods.append(sys.modules["modules." + mod].initClass())
            logger.info(f'Successfully loaded initClass() for: {mod}')
        except AttributeError:
            logger.info(f'No initClass() found for: {mod}')

    logger.info(f'Loaded {len(botMods)} mods for Egg_Bot')
    return


def reloadClasses():
    """ Reload classes that allow a forced reload """
    global botMods
    for mod in botMods:
        try:
            if mod.allowReload:
                mod.loadConfig(mod.activeConfig)
        except AttributeError:
            continue
    return


def dropClasses():
    """ Drops (destroys) all class instances. """
    global botMods
    for x in range(0, len(botMods)):
        botMods[x] = None
    return


def main():
    """
        Arrakis teaches the attitude of the knife — chopping off what’s
        incomplete and saying: "Now it’s complete because it’s ended here."
    """
    loadCore()
    logging_init.config_logger('./config/logging_config.json', LOGLEVEL)
    logger.info('Loading secrets...')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    if not(DISCORD_TOKEN):
        logger.critical('Failed to load secrets. Closing')
        exit()
    logger.info('Secrets loaded, assets contained, plans are hatching...')
    logger.info('Cracking the module carton open for more supplies...')
    loadClasses()
    logger.info('Loaded yolk configuration file.')
    logger.debug(f'{VERSION} {VERSION_NAME} {LOGLEVEL}')
    logger.info('Hatch cycle started.')
    logger.info(f'Shell version: {VERSION}, {VERSION_NAME}')
    logger.info('Hatching onto Discord now.')

    # dClient.run(DISCORD_TOKEN)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(dClient.start(DISCORD_TOKEN))
    except KeyboardInterrupt:
        logging.info('KeyboardInterrupt detected. Logging out')
        loop.run_until_complete(dClient.logout())
        # cancel all tasks lingering
    finally:
        loop.close()

    return


if __name__ == '__main__':
    exit(main())

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
