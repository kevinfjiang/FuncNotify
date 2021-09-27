"""Template to create a notify class out of that outlines the specific 
criteria to noitfy someone. 

`xNotifyx` is a shorthand name for whatever notification method. Preferably one word and in UpperCamelCase.
Examples: Print, Text, Slack, Teams, WhatsApp...
Once you come up with a name and create a copy of this file, do command-fn-F2 and replace all of `xNotifyx`

Naming: Name the file `xNotifyx`Method.py`. This is important because the __init__ only pulls files that end in Method.py, which is why
`NotifyDecorators.py`, `NotifyMethods.p`y, and `TemplateMethod.py` don't get pulled because they lack the `...Method.py`. Note this file ends in a
`_.py` which is why it won't be auto imported

`NotifyMethods.py` has much of the brains of the operation, look in there for the abstract methods by ctrl-f `@abstractmethod`. Alternatively, 
just look at the template. 

The specific notify function will make it easier on end users to see what specific arguments to specify for your function to help it.

NOTE replace anything in brackets
"""
    
import os # Grabbing environment variables

from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for `xNotifyx`. Include why each package is here

def time_xNotifyx(function=None, dot_env=True,  *args, **kwargs): # Include something to check the rest of the arguments in the word
    """Decorator specific for xNotifyx, if no credentials specified, it wil fill in with .env variables. 
    The import is necessary and cheap due to python's import system. If anyone has a solution please lmk!!
    
    Args:
        function (function, optional): In case you want to use time_func as a pure decorator without argumetns, Alert serves as 
        the function. Defaults to None.
        NOTE add all key word arguments that could be used by the class to enable more accurate mesaging
        [variable] ([type], optional): [Summary]. Defaults to [Default]"""
    return time_func(function=function, dot_env=dot_env, funcSpecify="xNotifyx", *args, **kwargs) 

class xNotifyxMethod(NotifyMethods):
    """[Summaraize exactly how this Method will notify the end user and what platform.]
    """    

    def __init__(self, *args, **kwargs):
        """Specify key word arguments in the init as var=xyz and define them as instances
        """        
        super().__init__(*args, **kwargs)

    def _set_credentials(self, token: str=None, *args, **kwargs)->None:
        """If instance variables are not defined, define environment variables here
        Then add the env variables to my.env for your specific environment variables
        Finally add the variable name and equal sign in a new section in template.env 
        for future use. Extension of __init__
        """   
        self.token = self.str_or_env(token, "TOKEN") # Example use with a random token
    def add_on(self)->str:
        """Specify an addon to tack on to the end of each message, solely a cosmetic thing
        If there are big issues with this, ie some platforms are much more annoying I can change 
        this 
        """
        return ""        
        
    def send_message(self, MSG: str):
        try:
            """Specify the API and set up of sending a singular message"""
            pass         
        except Exception as ex:
            """Handle the error somewhat or don't. If you want to add more information do it here"""       
            raise ex
