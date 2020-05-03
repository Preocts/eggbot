"""
Egg Bot, Discord Modular Bot

Created by Preocts
preocts@preocts.com | Preocts#8196 Discord
Permissions integer assumed: 502848 / 268807234
https://discordapp.com/api/oauth2/authorize?client_id=650127838552522753&permissions=268807234&scope=bot

https://github.com/Preocts/Egg_Bot

"""

# Additional imports
import os
import discord
import json
import logging
import modules
import asyncio
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()
BOT_OWNER = os.getenv('BOT_OWNER')
VERSION = None
VERSION_NAME = None
LOGLEVEL = None

# Global Classes from modules
# One day I'll figure out how to do these dynamically and the world will fall!
JA = None
SB = None
BC = None
GM = None

dClient = discord.Client(status='online',
                         activity=discord.Activity(type=2, name="you breathe"))

# ON READY - connection established
@dClient.event
async def on_ready():
    logger.info('Egg hatched! Connection Established!')
    logger.info('Egg successfully hatched.')
    logger.info('Connection to Discord Established.')
    logger.info('Available Guilds:')
    for guild in dClient.guilds:
        logger.info(f'\t{guild}')
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

    logger.info(f'Member Join: Display Name: {member.display_name}'
                f' | User ID: {member.id}'
                f' | Account Created: {member.created_at}'
                f' | Guild: {member.guild.name}')

    # These should be in a config - FUTURE MODULE replaceTags
    lsHolders = ['[MENTION]', '[USERNAME]', '[GUILDNAME]', '\\n']
    lsMember = [member.mention, member.display_name,
                member.guild.name, '\n']

    # joinActions call - messages only (no actions taken)
    jaResults = JA.getJoinMessage(str(member.guild.id), str(member.id))

    if jaResults["status"]:
        for a in jaResults["response"]:
            if not(len(a["message"])):
                logger.warning('Blank message found, skipping')
                continue
            # Make replacements for tags - MOVE TO MODULE IN FUTURE
            for rp in lsHolders:
                a["message"] = a["message"].replace(rp, lsMember[lsHolders.index(rp)])  # noqa: E501
            if a["channel"]:
                logger.info(f'Sending Chat message to channel: {a["channel"]}')
                chatRoom = discord.utils.get(member.guild.channels,
                                             id=a["channel"])
                if not(chatRoom):
                    logger.warning(f'Channel not found: {a["channel"]}')
                else:
                    await chatRoom.send(a["message"])
            else:
                logger.info(f'Sending DM message to: {member.name}')
                await member.create_dm()
                await member.dm_channel.send(a["message"])

# ON MESSAGE - Bot Commands
@dClient.event
async def on_message(message):
    """ Event triggers on every new message bot can see """

    # Ignore messages by bot account
    if message.author == dClient.user:
        return False

    if str(type(message.channel)) == "<class 'discord.channel.TextChannel'>":
        channelType = "text"
    elif str(type(message.channel)) == "<class 'discord.channel.DMChannel'>":
        channelType = "dm"
    else:
        # Bot doesn't support Group private chats
        return False

    if str(message.author.id) == BOT_OWNER:
        # Disconnect - System command
        if message.clean_content == "egg!disconnect":
            classHandler("drop")  # Save and drop our classes
            if channelType == "text":
                await message.delete()
            await dClient.close()
            return False
        # Reload Configurations - System command
        if message.clean_content == "egg!reloadAll":
            classHandler("load")
        # if message.clean_content == "egg!testjoin":
        #     await on_member_join(dClient.get_guild(621085335979294740).get_member(int(BOT_OWNER)))  # noqa: E501

    if channelType == "text":
        # guildMetrics Block - The egg watches. The egg knows.
        GM.logit(message.guild.id, message.guild.name, message.author.id,
                 message.author.name, message.author.display_name,
                 message.clean_content)

        # ShoulderBird Block - Alerting for custom search strings
        results = SB.birdCall(str(message.guild.id), str(message.author.id),
                              message.clean_content)
        if results["status"]:
            birds = results["response"]
            for feathers in birds:
                bird = discord.utils.get(message.guild.members,
                                         id=feathers)
                # Anti-snooping: Stop bird chirping if user isn't in channel
                snack = discord.utils.find(lambda m: m.id == feathers,
                                           message.channel.members)
                logger.debug(f'Anti-snoop: {feathers} - {snack}')
                if bird and snack:
                    await bird.create_dm()
                    await bird.dm_channel.send('Mention alert: **' +
                                               str(message.author.display_name)
                                               + '** mentioned you in **' +
                                               message.channel.name +
                                               '** saying: \n`' +
                                               message.clean_content + '`')

        # basicCommand Processing
        results = BC.commandCheck(str(message.guild.id),
                                  str(message.channel.id),
                                  message.author.roles,
                                  str(message.author.id),
                                  message.clean_content)
        if results["status"]:
            await message.channel.send(results["response"])
        else:
            logger.debug(f'commandCheck False: {results["response"]}')

    if channelType == "dm":
        # Add message logging here for DM's to the bot
        pass

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


def classHandler(action: str):
    """ Handles the classes for the bot -=-=One day this will be automatic=-=-

        Args:
            action: One of two actions: Load, Drop

        Returns:
            None

        Raises:
            None
    """

    action = action.lower()
    global JA
    global SB
    global BC
    global GM

    if action == "load":
        if JA:
            JA.loadConfig()
        else:
            JA = modules.joinActions.joinActions()
    else:
        JA = None

    if action == "load":
        if SB:
            SB.loadConfig()
        else:
            SB = modules.shoulderBird.shoulderBird()
    else:
        SB = None

    if action == "load":
        if BC:
            BC.loadConfig()
        else:
            BC = modules.basicCommands.basicCommands()
    else:
        BC = None

    if action == "load":
        if GM:
            GM.loadConfig()
        else:
            GM = modules.guildMetrics.guildMetrics()
    else:
        GM = None

    return


def main():
    """
        Arrakis teaches the attitude of the knife — chopping off what’s
        incomplete and saying: "Now it’s complete because it’s ended here."
    """
    loadCore()
    modules.logging_init.logINIT(LOGLEVEL)
    logger.info('Loading secrets...')
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    if not(DISCORD_TOKEN):
        logger.critical('Failed to load secrets. Closing')
        exit()
    logger.info('Secrets loaded, assets contained, plans are hatching...')
    logger.info('Cracking the module carton open for more supplies...')
    classHandler("load")
    logger.info('Loaded yolk configuration file.')
    logger.debug(f'{VERSION} {VERSION_NAME} {LOGLEVEL}')
    logger.info(f'Hatch cycle started.')
    logger.info(f'Shell version: {VERSION}, {VERSION_NAME}')
    logger.info('Hatching onto Discord now.')

    # import time
    # classHandler("drop")
    # time.sleep(3)
    # exit()

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
