import logging

logger = logging.getLogger("default")  # Module logger


def isInt(checkvalue) -> bool:
    try:
        int(checkvalue)
    except ValueError:
        return False
    return True
