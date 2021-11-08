"""Print Messages to console
Setup:
    None necessary

"""
import FuncNotify.NotifyMethods as NotifyMethods # Using the predefined functions from the abstract class
# import FuncNotify.NotifyDecorators as NotifyDecorators // Not used

class PrintMethod(NotifyMethods.NotifyMethods):
    """Default print message, only notification is a print in terminal
    """    

    __slots__ = ("verbose") # List all instance variables here in string form, saves memory
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _set_credentials(self, verbose: bool=True, *args, **kwargs):
        self.verbose = self._type_or_env(verbose, "VERBOSE", bool)
        """Whether to print to the console or not"""        
    def _send_message(self, MSG: str):
        if self.verbose:
            print(MSG)
