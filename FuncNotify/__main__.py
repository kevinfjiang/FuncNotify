"""Call this module `FuncNotify` to be able to time scripts as well as functions
Note compiling function time may be counted, which is why some timings may 
appear to be innacurate
"""

import argparse
import subprocess
import ast

import re

from FuncNotify.NotifyDecorators import time_func

NO_ARGS_ERROR         = "No arguuments remianing to be exectued, confirm " \
                        "the desired execution is in the proper format"
COLLECTION_ARGS_ERROR = "Collection Argument not closed properly, " \
                        "check for hanging identifiers"

class ParseKwargs(argparse.Action):
    """Parses for the format `arg=val` parses for either strings or bools exclusively, 
    no ints. If it paressess a val that doesn't have a `=`, it's added to the unparse. 
    Wrapped to nobody can access this as it's exclusive to parsing. Used by argparse
    
    `__call__()` parses args into their proper formats, whether it's a kwarg, collection or a command"""    
    translation_dict = {"true" : True,
                        "True" : True,
                        "false": False,
                        "False": False}
    """ Translates string bools to bools"""    
    class CollectionParse:
        """Class used to parse string representations of collections
        Does so safety with ast.literal_eval and ensures that all collections
        are cloesd"""    
        CloseList = {'[': ']',
                    '{': '}',
                    '(': ')',
                    '"': '"',
                    "'": "'"}
        PairTypes = {*CloseList.keys(), *CloseList.values()}
        
        def __init__(self, key: str):
            self.collection_str_list = [] 
            self.remaining_pair_type = []
            self.key=key
        def build(self, value: str, PairTypes=PairTypes, CloseList=CloseList): 
            """Ensures that all characters that start something terminate, 
            Lowkey a compiler check, ensures the collection is written properly
            and all opens are closed. 

            Args:
                value (str): new string input
            """                
            for pair_type in filter(lambda x: x in PairTypes, value):
                if self.remaining_pair_type and pair_type == CloseList.get(self.remaining_pair_type[-1]):
                    self.remaining_pair_type.pop()  
                else:
                    self.remaining_pair_type.append(pair_type)

            self.collection_str_list.append(value)
            return not self.remaining_pair_type
        def eval_(self):
            """Evaluates the collecte list and returns the collection
            Raises:
                Exception: Depending on problems with the string, \
                like compile errors
            """             
            return ast.literal_eval("".join(self.collection_str_list))
        def __bool__(self):
            """Saw in video, faster than bool(list) apparently"""
            return not not self.remaining_pair_type
            
    def add_kwarg(self, namespace, key, value):
        """Adds args to args.kwargs so it can be passed into the decorator"""            
        if key in getattr(namespace, self.dest): # If key in list
            if isinstance(getattr(namespace, self.dest)[key], list):
                getattr(namespace, self.dest)[key].append(value) # Adds to list
            else:
                getattr(namespace, self.dest)[key] = [getattr(namespace, self.dest)[key], value] # creates list
        else:
            getattr(namespace, self.dest)[key] = value
        
    def add_collection_parse(self, namespace, CollectParseObj, value):
        """Adds value to CollectParseObj, if it is a proper collection, 
        it will evaluate and add it to the kwargs
        """            
        if CollectParseObj.build(value):
            self.add_kwarg(namespace, CollectParseObj.key, CollectParseObj.eval_())
    
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        setattr(namespace, "_unrecognized_args", list())
        CollectParseObj=ParseKwargs.CollectionParse("")
        
        for value in values:
            if not CollectParseObj and re.match('^[a-zA-Z0-9_]+(=[^\n\t\r]+)$', value):
                key, value = value.split('=')
                if value[0] in ["[", "{", "("]:
                    # Occurs only if the first char is a collection object
                    CollectParseObj=ParseKwargs.CollectionParse(key)
                    self.add_collection_parse(namespace, CollectParseObj, value)
                else:
                    value = ParseKwargs.translation_dict.get(value, value) # Ensures bools are properly parsed
                    self.add_kwarg(namespace, key, value)
            elif CollectParseObj: # Count repeats of the first guy and subtract count of the other guy
                self.add_collection_parse(namespace, CollectParseObj, value)
            else:
                getattr(namespace, "_unrecognized_args").append(value)
        if CollectParseObj:
            raise argparse.ArgumentError(COLLECTION_ARGS_ERROR)

def main(): 
    """Parses the commandline input for the executable command and kwargs 
    separated by the indicatiorr `-k` or `--kwargs` and `arg=val` syntax.
    One can pass collections as strings as kwargs but must wrap the object in 
    double quotes.
    
    Uses `subprocess.run()` to execute the command input.

    Raises:
        argparse.ArgumentError: If either a collection isn't closed \
        or no command is left after parsing, ArgumentError will be raised
    """       

    parser = argparse.ArgumentParser(
        description="FuncNotify - Be notified securely when your function/script completes. " \
                    "Store all your variables in a `.env` file and let us do the work for you " \
                    "To input arguments, use --kwargs followed by `arg=value`")
    parser.add_argument('-k', '--kwargs', nargs='*', action=ParseKwargs,
                        help="Input as many kwargs as needed  to specify exactly how you want to be notified " \
                        "Make sure all inputs are in the format `var`=`value` which all values " \
                        "will be interpreted as strings. To input sets, dicts or lists, it's best wrap the " \
                        "entire collection in double quotes and strings within in single quotes") 
    
    args, remaining_args = parser.parse_known_args()
    kwargs = {**args.kwargs} if args.kwargs else {}
    
    # Runs sthe remaining_args as if they were ran in the terminal
    def sub_run(): return subprocess.run(remaining_args, check=True)     
        
    sub_run.__name__ = " ".join(remaining_args) # Setting changing name for clarity
    
    # Faster than using decorator, also using wacky lambda to raise Exceptions properly 
    time_func(sub_run, **kwargs)() if remaining_args else (lambda: (_ for _ in ()).throw(
                                                           argparse.ArgumentError(NO_ARGS_ERROR)))()

if __name__ == "__main__":
    """When `FuncNotify` is called from the CLI, we execute main()"""
    main() 