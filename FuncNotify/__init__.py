from os.path import dirname, basename, isfile, join
import glob
import importlib

module_list = glob.glob(join(dirname(__file__), "*Method.py"))
MODULES = [basename(f)[:-3] for f in module_list if isfile(f)]

def import_all(modules: list):
    """Imports of a module, similar to `from package import *` but specifically for this package

    Args:
        modules (list[str]): A file name in `FuncNotify` directoory/package
    """    
    for mod in modules:
        try:
            module = importlib.import_module(f'FuncNotify.{mod}') 
            globals().update({k: v for (k, v) in module.__dict__.items() if not k.startswith('_')})
        except Exception as ex:
            print(f"Unable to import {mod} due to the following error")
            print(f"[ERROR] Exception: {ex}")

import_all(MODULES)
from FuncNotify.NotifyDecorators import *