"""Call this wiht `FuncNotify` to be able to time scripts as well as functions
Note compiling function time may be counted, which is why some timings may 
appear to be innacurate
"""

import argparse
import subprocess

import re

from FuncNotify import *




def main():
    parsed_remain_arg = []
    class ParseKwargs(argparse.Action):
        """Parses for the format `arg=val` parses for either strings or bools exclusively, no ints
        If it paressess a val that doesn't have a `=`, it's ade to the parsed_remain_arg list
        """    
        translation_dict = {"true":  True,
                            "True":  True,
                            "false": False,
                            "False": False,}
        
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, dict())
            for value in values:
                
                if re.match('^[a-zA-Z0-9_]+(=[^\s]+)$', value):
                    key, value = value.split('=')
                    value = ParseKwargs.translation_dict.get(value, value) # Ensures bools are properly parsed
                    
                    if key in getattr(namespace, self.dest): # If key in list
                        if isinstance(getattr(namespace, self.dest)[key], list):
                            getattr(namespace, self.dest)[key].append(value) # Adds to list
                        else:
                            getattr(namespace, self.dest)[key] = [getattr(namespace, self.dest)[key], value] # creates list
                    else:
                        getattr(namespace, self.dest)[key] = value
                else:
                    parsed_remain_arg.append(value) 
    
    parser = argparse.ArgumentParser(
        description="FuncNotify - Be notified securely when your function/script completes. " \
                    "Store all your variables in a `.env` file and let us do the work for you " \
                    "To input arguments, use --kwargs followed by `{arg}=value`")
    parser.add_argument('-k', '--kwargs', nargs='*', action=ParseKwargs)
    
    args, remaining_args = parser.parse_known_args()
    
    kwargs = {**args.kwargs} if args.kwargs else {}
    
    def sub_run(): 
        if remaining_args or parsed_remain_arg: # Some non kwargs may get parsed but get recollected here
            return subprocess.run([*remaining_args, *parsed_remain_arg], check=True)
        else:
            print("No command specified to be executed")
    
    sub_run.__name__ = " ".join([*remaining_args, *parsed_remain_arg]) # Setting func.__name__ to this for clarity
    time_func(sub_run, **kwargs)() # Faster than using decorator, less down time


if __name__ == "__main__":
    """When `FuncNotify` is called from the CLI, we go to this function"""
    main() 