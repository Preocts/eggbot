""" Helper functions for loading and saving to a given json config

    Created by Preocts
    preocts@preocts.com | Preocts#8196 Discord
    https://github.com/Preocts/Egg_Bot

"""
import json
import logging

logger = logging.getLogger(__name__)


class JSON_Config_Error(Exception):
    """ Custom Raise Class """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'JSON_Config_Error, {self.message}'
        else:
            return 'JSON_Config_Error, an error has been raised'


def loadConfig(inputFile: str) -> dict:
    """ Loads provided JSON file into memory as a dictionary

        Args:
            inputFile: File path and name to JSON file

        Returns:
            Contents of JSON file as dict

        Raises:
            JSON_Config_Error:
                Raised when there is an issue loading the given JSON
    """
    json_file = {}
    try:
        with open(inputFile) as file:
            json_file = json.load(file)
    except json.decoder.JSONDecodeError:
        # logger.error(f'Config file empty ', exc_info=True)
        raise JSON_Config_Error(f"Config file is empty: {inputFile}")
    except FileNotFoundError:
        logger.error(f'Config file not found: {inputFile}', exc_info=True)
    logger.info(f'Succes: Loaded config file: {inputFile}')
    return json_file


def saveConfig(json_config: dict, outputFile: str, raw: bool = False) -> bool:
    """ Writes provided JSON content to file

        Args:
            json_config: Inforamtion to write to file
            outputFile: File path and name to JSON file

        Returns:
            True

        Raises:
            JSON_Config_Error:
                Raised when there is an issue saving to the given file
    """

    try:
        with open(outputFile, 'w') as file:
            if raw:
                file.write(json.dumps(json_config))
            else:
                file.write(json.dumps(json_config, indent=4))

    except OSError:
        # logger.error(f'File not be opened: {outputFile}', exc_info=True)
        raise JSON_Config_Error(f"Could not open target file: {outputFile}")
    logger.info(f'Success: Config saved to: {outputFile}')
    return True

# May Bartmoss have mercy on your data for running this bot.
# We are all only eggs
