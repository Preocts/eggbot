"""
Provide a list of extentions for commands and cogs to load

Author  : Preocts
Discord : Preocts#8196
Git Repo: https://github.com/Preocts/eggbot
"""
import importlib
import inspect
import pathlib
from typing import List


def get_files(extspath: str) -> List[pathlib.Path]:
    """Pull all *.py files"""
    exts = pathlib.Path(extspath).glob("*.py")
    return [name for name in exts if name.is_file()]


def convert_to_module_path(filepath: pathlib.Path) -> str:
    """converts path to an import reference"""
    parts = list(filepath.parts)
    module = (parts.pop()).replace(".py", "")
    return ".".join(parts) + f".{module}"


def load_ext(extspath: str) -> List[str]:
    """Identify all valid extentions in given exts path"""
    ext_list: List[str] = []
    for filepath in get_files(extspath):
        module_path = convert_to_module_path(filepath)
        importmod = importlib.import_module(module_path)
        if not inspect.isfunction(getattr(importmod, "setup", None)):
            continue
        ext_list.append(module_path)

    return ext_list
