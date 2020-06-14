import logging

logger = logging.getLogger(__name__)  # Create module level logger


def isInt(checkvalue) -> bool:
    try:
        int(checkvalue)
    except ValueError:
        return False
    return True
