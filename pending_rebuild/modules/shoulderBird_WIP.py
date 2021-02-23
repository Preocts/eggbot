# -*- coding: utf-8 -*-
"""
    ShoulderBird is tool that add DM pings on keyword from chat

    Alerts a user when a keyword of their choice is said in any chat
    that is being watched by the bot. The keywords are scanned by regex
    with the messege's content being relayed to the user via a DM from
    the bot when the regex finds a match.

    Created by Preocts
        Preocts#8196 Discord
        https://github.com/Preocts/Egg_Bot
"""

import re
import logging
from eggbot.utils import eggUtils

logger = logging.getLogger(__name__)  # Create module level logger


class shoulderBird:
    """ShoulderBird scans incomming discord.onmessage events for keywords

    Keywords are defined from the configuration file loaded on the
    initialization of a class instance. Guilds and users are stored by
    their ID in string form.

    This class was designed to work inline with Discord.py library but only
    uses the library through arguments passed in the method onMessage().

    Class Attributes:
        name [str] : Name of class
        version [str] : Version of module release
        allowReload [bool] : Flag for external use. If ture this module is
            save to reload the config at anytime during use without risk
            of data loss.
        instCount [int] : Increment counter of how many instances are declared

    Attributes:
        sbConfig [dict] : Stores the instances copy of the configuration
        activeConfig [str] : Path and filename of the loaded configuration
    """

    name = "shoulderBird"
    version = "v1.0.0"
    allowReload = True
    instCount = 0

    # ╔════════════*.·:·.✧    ✦    ✧.·:·.*════════════╗
    #            Standard Eggbot module setup
    # ╚════════════*.·:·.✧    ✦    ✧.·:·.*════════════╝
    def __init__(self):
        """INIT"""
        logging.info("Start: Initializing shoulderBird")
        self.sbConfig = {}
        self.activeConfig = ""
        self.loadConfig()
        shoulderBird.instCount += 1
        logger.info(f"Config loaded with {len(self.sbConfig)}")
        return

    def __str__(self):
        return str(self.sbConfig)

    def __bool__(self):
        if len(self.sbConfig):
            return True
        return False

    __nonzero__ = __bool__

    def gagBird(self, user: str, target: str) -> dict:
        """Toggles a given target for a given guild to be ignored

        While logging messages may capture messages from ignored users if
        the logging levels are set low enough, ignored users will not trigger
        a shoulderBird alert.

        Hopefully, someday, Discord figures out the simple application of
        display: none; to hide blocked users in the channel history. >:V

        Args:
            [str] : User ID to assign config to
            [str] : User ID to ignore

        Returns:
            [dict] : {"status": [bool], "response": [str]}
        """
        logger.debug(f"[START] gagBird : {user}, {target}")
        response = None
        for guild, values in self.sbConfig.items():
            if user in values:
                # Unignore
                if target in self.sbConfig[guild][user]["ignore"]:
                    idx = self.sbConfig[guild][user]["ignore"].index(target)
                    self.sbConfig[guild][user]["ignore"].pop(idx)
                    response = "User is no longer ignored in all guilds"
                    continue
                self.sbConfig[guild][user]["ignore"].append(target)
                response = "User is now ignored in all guilds"
        logger.debug(f"[FINSIH] gagBird : {response}")
        if response is None:
            return {"status": False, "response": "You have no birds to edit"}
        return {"status": True, "response": response}

    # ╔════════════*.·:·.✧    ✦    ✧.·:·.*════════════╗
    #              Discord.py hook methods
    # ╚════════════*.·:·.✧    ✦    ✧.·:·.*════════════╝
    async def onMessage(self, **kwargs) -> bool:
        """Hook method to be called from core script on Message event

        Keyword Args:
            message [discord.message] : a discord.message class
            client [discord.client] : Active discord client reference

        Returns:
            None
        """
        logger.debug("[START] onMessage : ")
        Supported_Channels = (
            "<class 'discord.channel.DMChannel'>",
            "<class 'discord.channel.TextChannel'>",
        )
        message = kwargs.get("message")
        client = kwargs.get("client")

        if client is None:
            return

        if str(type(message.channel)) not in Supported_Channels:
            logger.debug("[FINISH] onMessage : Channel type not support")
            return

        # DM Channel catch
        if str(type(message.channel)) == Supported_Channels[0]:  # DM channel
            # Special case !help command
            if message.clean_content.lower() == "!help":
                response = "ShoudlerBird installed: **sb!help** for details"
                await message.author.dm_channel.send(response)
                return

            # Process possible ShoulderBird Commands
            if message.clean_content[0:3].lower() == "sb!":
                response = self.commands(message, kwargs["client"])
                if response:
                    await message.author.dm_channel.send(response)
                return
            return

        # ╔════════════*.·:·.✧    ✦    ✧.·:·.*════════════╗
        #    ShoulderBird - Alerting for search strings
        # ╚════════════*.·:·.✧    ✦    ✧.·:·.*════════════╝
        results = self.birdCall(
            str(message.guild.id),
            str(message.author.id),
            message.clean_content,
        )
        if results["status"]:
            birds = results["response"]
            for feathers in birds:
                bird = message.guild.get_member(feathers)
                # Anti-snooping: Stop bird chirping if user isn't in channel
                # This might need to be more efficient in the future
                for m in message.channel.members:
                    if m.id == feathers:
                        snack = m.id
                        break

                logger.debug(f"Anti-snoop: {feathers} - {snack}")
                if bird and snack:
                    await bird.create_dm()
                    msg = "".join(
                        [
                            "Mention alert: **",
                            str(message.author.display_name),
                            "** mentioned you in **",
                            message.channel.name,
                            "** saying:\n`",
                            message.clean_content,
                            "`",
                        ]
                    )
                    await bird.dm_channel.send(msg)
        logging.debug("[FINISH] onMessage : ")
        return

    def commands(self, message, dClient) -> str:
        """ Process any DM commands sent """

        # strip the !trigger word and leading space out of the message
        cmdTrig = message.clean_content.split(" ")[0].lower()

        if cmdTrig == "sb!set":
            # sb!set [guild] = [body]
            if "=" not in message.clean_content:
                return (
                    "Error: Formatting incorrect. \n"
                    "```sb!set [Guild Name or ID] = [regular expression]```"
                )
            # We need to pull the [guild] provided and do two things,
            # 1) Confirm bot is in that guild
            # 2) Ensure we are using a guild.id and not a name
            cmdTarg = message.clean_content.split("=")[0].strip(cmdTrig).strip()  # noqa
            guildID = None
            for g in dClient.guilds:
                # Provided a guild ID
                if eggUtils.isInt(cmdTarg) and g.id == int(cmdTarg):
                    guildID = str(g.id)
                    break
                # Provided a guild Name
                if not (eggUtils.isInt(cmdTarg)) and g.name == cmdTarg:
                    guildID = str(g.id)
                    break
            if guildID is None and len(cmdTarg) != 0:
                return f"Error: I'm not that guild: {cmdTarg}"

            result = self.putBird(guildID, message)
            self.saveConfig()
            return result["response"]

        if cmdTrig == "sb!on":
            # Turn on all birds for user
            result = self.toggleBird(str(message.author.id), True)
            self.saveConfig()
            return result["response"]

        if cmdTrig == "sb!off":
            # Turn on all birds for user
            result = self.toggleBird(str(message.author.id), False)
            self.saveConfig()
            return result["response"]

        if cmdTrig == "sb!ignore":
            # sb!ignore [name/ID]
            # Confirm if the name/ID is in the guild provided
            cmdBody = message.clean_content.split()[1:][0]
            if not (cmdBody):
                return (
                    "Error: Formatting incorrect. \n"
                    "```sb!ignore [username or ID to ignore]```"
                )

            # Find this user ID if available
            # TODO: This will need some improvements for speed
            targID = None
            for user in dClient.users:
                # Provided a user ID
                if eggUtils.isInt(cmdBody) and user.id == int(cmdBody):
                    targID = str(user.id)
                    break
                # Provided a user Name
                if not (eggUtils.isInt(cmdBody)) and user.name == cmdBody:
                    targID = str(user.id)
                    break
            if targID is None:
                return (
                    f"Error: Can't find {cmdBody}. Be sure you are "
                    "providing either their Username without the #0000 "
                    "or their user ID."
                )
            result = self.gagBird(str(message.author.id), targID)
            self.saveConfig()
            return result["response"]

        if cmdTrig == "sb!delete":
            # sb!remove
            result = self.delBird(str(message.author.id))
            self.saveConfig()
            return result["response"]

        if cmdTrig == "sb!list":
            # sb!list
            result = self.listBirds(str(message.author.id))
            if result["status"]:
                dmmessage = ["List of birds:\n```\n"]
                for bird in result["response"]:
                    guild = dClient.get_guild(int(bird[0]))
                    guild = guild.name if guild is not None else "Unknown"
                    dmmessage.append(f"{guild} : {bird[1]}\n")
                dmmessage.append("```")
                return "".join(dmmessage)
            else:
                return result["response"]

        if cmdTrig == "sb!help":
            # sb!help
            response = (
                "Command List: *There is no undo button!*\n```"
                "+ sb!list [guild name/ID]\n"
                "\tLists stored searches from all guilds\n"
                "+ sb!on\n"
                "\tTurns ShouldBird on for all guilds you have\n"
                "+ sb!off\n"
                "\tTurns ShouldBird off for all guilds you have\n"
                "+ sb!set [guild name or ID] = [RegEx]\n"
                "\tSets a user's RegEx search for given guild\n"
                "\tguild name is case sensitive. If you have dev\n"
                "\tmode on you can provide the guild ID\n"
                "+ sb!ignore [user name (not nickname) or ID]\n"
                "\tToggles a user to be ignored by ShoulderBird\n"
                "\tacross all guilds you have a search in. If they\n"
                "\tare already ignored, they will be unignored\n"
                "\tUser name excludes the #0000 numbers\n"
                "+ sb!delete\n"
                "\tDeletes all your birds. ***There is no undo!***\n"
                "+ sb!help\n"
                "\tDisplays this help box\n```"
            )
            return response


# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
