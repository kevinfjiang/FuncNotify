from os.path import dirname, basename, isfile, join
import glob
import importlib

modules = glob.glob(join(dirname(__file__), "*Method.py"))

for mod in [basename(f)[:-3] for f in modules if isfile(f)]:  # auto imports all files ending in *Method.py
    try:
        module = importlib.import_module(f'FuncNotify.{mod}') # TODO find a way too impoort the small functions!
        globals().update(
            {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') else 
                {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
            })
    except Exception as ex:
        print(f"Unable to import {mod} due to the following error")
        print(f"[ERROR] Exception: {ex}")
# One i have a bunch and am adding less to this, i'll attempt to hard code these values 
# so we don't have the weird import errors
# Automates automatic imports

from FuncNotify.NotifyDecorators import *