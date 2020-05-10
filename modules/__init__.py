# Hard import the following
from os import listdir
import importlib

# Gather modules
mypath = "./modules"
MODULE_NAMES = []
for file in listdir(mypath):
    if file.endswith('.py') and file[0] != "_":
        importlib.import_module("modules." + file[:-3])
        MODULE_NAMES.append(file[:-3])
