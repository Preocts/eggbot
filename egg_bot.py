"""
Egg Bot, Discord Modular Bot

Created by Preocts
preocts@preocts.com | Preocts#8196 Discord
Permissions integer assumed: 502848

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
ENVIRO = None
LOGLEVEL = None

# Global Classes from modules
# One day I'll figure out how to do these dynamically and the world will fall!
JA = None
SB = None
BC = None

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
async def on_member_join(dMember):
    """ Handle the event of a user joining the guild """

    logger.info(f'Member Join: Display Name: {dMember.display_name}'
                f' | User ID: {dMember.id}'
                f' | Account Created: {dMember.created_at}'
                f' | Guild: {dMember.guild.name}')

    """ joinActions Block

        This will need to be moved into the module for module level control
        features.

        Scans for active joinActions that relate to the member.guild.name that
        is provided. When found the message and/or action is taken in following
        order of operations:
        - Process invite then non-invite specific join actions
        - Order of operation during processing:
          - Apply role
          - Actions
          - DM Messages (find first order)
          - Channel Messages (find first order)
    """

    results = JA.readAll(dMember.guild.name)
    if not(results["status"]):
        logger.info(f'Guild not configured: {dMember.guild.name}')
    actions = results["response"]
    logger.debug(f'{actions}')
    # These should be in a config
    lsHolders = ['[MENTION]', '[USERNAME]', '[GUILDNAME]', '\\n']
    lsMember = [dMember.mention, dMember.display_name,
                dMember.guild.name, '\n']
    for a in actions:
        if a["active"] and a["channel"] == "":
            logger.info(f'Sending DM welcome message to {dMember.name}')
            DM = a["message"]
            await dMember.create_dm()
            for rp in lsHolders:
                DM = DM.replace(rp, lsMember[lsHolders.index(rp)])
            if len(DM) > 0:
                await dMember.dm_channel.send(str(DM))
        elif a["active"] and len(a["message"]) > 0:
            logger.info('Sending Chat welcome message to '
                        f'{a["channel"]} | {dMember.display_name}')
            chatRoom = discord.utils.get(dMember.guild.channels,
                                         name=a["channel"])
            if chatRoom:
                CH = a["message"]
                for rp in lsHolders:
                    CH = CH.replace(rp, lsMember[lsHolders.index(rp)])
                await chatRoom.send(CH)

# ON MESSAGE - Bot Commands
@dClient.event
async def on_message(message):
    """ Event triggers on every new message bot can see """

    # Ignore messages by bot account
    if message.author == dClient.user:
        return False

    if str(message.author.id) == BOT_OWNER:
        # Disconnect - System command
        if message.clean_content == "egg!disconnect":
            classHandler("drop")  # Save and drop our classes
            await message.delete()
            await dClient.close()
            return False
        # Reload Configurations - System command
        if message.clean_content == "egg!reloadAll":
            classHandler("load")

    if str(type(message.channel)) == "<class 'discord.channel.TextChannel'>":

        # ShoulderBird Block - Alerting for custom search strings
        results = SB.birdCall(message.guild.name, message.author.name,
                              message.clean_content)
        if results["status"]:
            bird = discord.utils.get(message.guild.members,
                                     name=results["response"])
            if bird:
                await bird.create_dm()
                await bird.dm_channel.send('Mention alert: **' +
                                           str(message.author.display_name) +
                                           '** mentioned you in **' +
                                           message.channel.name +
                                           '** saying: \n`' +
                                           message.clean_content + '`')

        # basicCommand Processing
        results = BC.commandCheck(message.guild.name, message.channel.name,
                                  message.author.roles.copy(),
                                  message.author.name, message.clean_content)
        if results["status"]:
            await message.channel.send(results["response"])
        else:
            logger.debug(f'commandCheck False: {results["response"]}')

    if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>":
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
            global ENVIRO
            ENVIRO = configs["CoreConfig"]["Environment"]
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
    logger.debug(f'{VERSION} {VERSION_NAME} {LOGLEVEL} {ENVIRO}')
    logger.info(f'Hatch cycle started.')
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
