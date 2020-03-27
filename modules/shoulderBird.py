""" ShoulderBird is a Discord channel alert tool

    Alerts a user when a keyword of their choice is said in any chat
    that is being watched by the bot.

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord

    Refactor: 03/23/2020
"""
import logging
import json
import re

logger = logging.getLogger(__name__)  # Create module level logger


class shoulderBird:
    """Defines the ShouldBird Object

        Config format:
        {
            "guildname" {
                "username": {
                    "regex": "Expression",
                    "toggle": Boolean
                }
            }
        }

        Definitions:
            Bird : A single search string in regEx
    """

    def __init__(self, inputFile="../config/shoulderBird.json"):
        """INIT"""
        self.shouldBird = {}
        self.activeConfig = ""
        self.loadConfig(inputFile)

    def getBirds(self, guildname: str) -> dict:
        """ Fetch all defined Birds from the config file """
        # Do we have this guild setup and is there anything there?
        if ((guildname in self.shoulderBird) and
           len(self.shoulderBird[guildname])):
            return self.shoulderBird[guildname]
        return False

    def getBird(self, guildname: str, username: str) -> dict:
        """ Fetch a single defined Bird from the config file """
        logger.debug(f'getBird call: {guildname} | {username}')
        if ((guildname in self.shoulderBird) and
           len(self.shoulderBird[guildname])):
            if username in self.shoulderBird[guildname]:
                if self.shoulderBird[guildname][username]["toggle"]:
                    return self.shoulderBird[guildname][username]["regex"]
        return False

    def putBird(self, guildname: str, username: str, regex: str) -> bool:
        """ Stores a Bird into the loaded config """
        # Literally just assign it. No gaurdrails at this time
        if not(guildname in self.shoulderBird):
            self.shoulderBird[guildname] = {}
        self.shoulderBird[guildname][username] = {}
        self.shoulderBird[guildname][username]["regex"] = regex
        self.shoulderBird[guildname][username]["toggle"] = False
        return True

    def delBird(self, guildname: str, username: str) -> bool:
        """ Removes a Bird from the loaded config """
        if guildname in self.shoulderBird:
            if username in self.shoulderBird[guildname]:
                del self.shoulderBird[guildname][username]
                return True
        return False

    def toggleBird(self, guildname: str, username: str,
                   update: bool = False) -> bool:
        """ Toggles ShoulderBird for a specific guild """
        # If the user isn't set, move on.
        if guildname in self.shoulderBird:
            if username in self.shoulderBird[guildname]:
                curToggle = self.shoulderBird[guildname][username]["toggle"]
                if curToggle:
                    if update:
                        curToggle = False  # Hide Bird Alerts
                else:
                    if update:
                        curToggle = True  # Send Bird Alerts
                self.shoulderBird[guildname][username]["toggle"] = curToggle
        return curToggle

    def birdCall(self, sMessage: str, sSearch: str) -> bool:
        """ Uses regEx to find defined keywords in a chat message

        Updates:
            Added 0.1.2 - Preocts - Start to create flexible bird
            Refactor 0.3.1 - Preocts - Moved to new Module

        Args:
            sMessage: The message being scanned (use message.clean_content)
            sSearch: The regEx string of the Bird

        Returns:
            True if keyword found
            False if keyword not found
        """

        findRg = re.compile(r'\b{}\b'.format(sSearch), re.I)
        found = findRg.search(sMessage)
        if found:
            return True
        return False

    def loadConfig(self, inputFile: str) -> dict:
        """ Loads shoulderBird configuration into memory"""

        try:
            with open(inputFile) as file:
                self.shoulderBird = json.load(file)
        except json.decoder.JSONDecodeError:
            logger.error(f'shoulderBird Config file empty ', exc_info=True)
        except FileNotFoundError:
            logger.error(f'shoulderBird Config file not found '
                         '{inputFile}', exc_info=True)
            try:
                open(inputFile, 'w')
            except OSError:
                logger.critical('shoulderBird failed to load. Closing. ',
                                exc_info=True)
                exit()
        self.activeConfig = inputFile
        return {"status": True, "response": "Config loaded"}

    def saveConfig(self, outputFile: str = None) -> dict:
        """ Writes shoulderBird configuration to disk """

        if not(outputFile) and len(self.activeConfig) > 0:
            outputFile = self.activeConfig
        else:
            logger.warning(f'saveConfig: No file give: {outputFile}')
            return {"status": False, "response": "Missing filename"}
        try:
            with open(outputFile, 'w') as file:
                file.write(json.dumps(self.shoulderBird, indent=4))
                logger.info(f'Success: shoulderBird config '
                            'saved to {outputFile}')

        except OSError:
            logger.error(f'shoulderBird Config file not saved to {outputFile}',
                         exc_info=True)
            return {"status": False, "response": "Error saving config"}
        return {"status": True, "response": "Config saved"}
