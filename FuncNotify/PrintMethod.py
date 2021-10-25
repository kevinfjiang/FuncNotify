from .NotifyMethods import *
from .NotifyDecorators import time_func

class PrintMethod(NotifyMethods):
    """Default print message, only notification is a print in terminal
    """    

    __slots__ = ("verbose") # List all instance variables here in string form, saves memory
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_credentials(self, verbose: bool=True, *args, **kwargs):
        self.verbose = self.type_or_env(verbose, "verbose", bool)
        
    def send_message(self, MSG: str):
        if self.verbose:
            print(MSG)
