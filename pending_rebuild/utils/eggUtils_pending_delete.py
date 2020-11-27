import os


def isInt(checkvalue) -> bool:
    try:
        int(checkvalue)
    except ValueError:
        return False
    return True


def abs_path(filepath: str) -> str:
    """ Returns path of given __file__ """
    dirpath = os.path.sep.join(filepath.split(os.path.sep)[:-1])
    return dirpath if dirpath else '.'
