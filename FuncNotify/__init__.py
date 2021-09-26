from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))

for mod in [basename(f)[:-3] for f in modules if isfile(f) and f.endswith ('Method.py')]:
    try:
        __import__("FuncNotify." + mod, locals(), globals())
    except Exception as ex:
        print(f"Unable to import {mod} due to the following error")
        print(f"[ERROR] Exception: {ex}")
# One i have a bunch and am adding less to this, i'll attempt to hard code these values 
# so we don't have the weird import errors
# Automates automatic imports
    
from FuncNotify.NotifyDecorators import *