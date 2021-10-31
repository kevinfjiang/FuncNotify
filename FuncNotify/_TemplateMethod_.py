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

NOTE replace anything that is `xNotifyx`
TODO do a cmd+F2 on `xNotifyx` to the desired method so it auto changes. After you can delete the intro, or change it to explain more
"""

from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for `xNotifyx`. Include why each package is here

def time_xNotifyx(func=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """TODO Decorator specific for xNotifyx, if no credentials specified, it wil fill in with .env variables. 
    
    Args:
        func (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): path to .env file. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updatess on 
        initialization. Defaults to False.
        
        Insert remaining args here
        NOTE add all key word arguments that could be used by the class to enable more accurate mesaging
        [variable] ([type], optional): [Summary]. Defaults to [Default]"""
    return time_func(func=func, NotifyMethod="xNotifyx", use_env=use_env, env_path=env_path, update_env=update_env, *args, **kwargs) 

class xNotifyxMethod(NotifyMethods):
    """TODO Summaraize exactly how xNotifyxMethod will notify the end user and what platform.
    """   
    
    __slots__ = ("__token") # List all instance variables here in string form, saves memory, 
                            # optional but highly reccomended, don't forget `__`

    def __init__(self, *args, **kwargs):
        """TODO Specify key word arguments in the init as var=xyz and define them as instances
        """        
        super().__init__(*args, **kwargs)

    def _set_credentials(self, token: str=None, *args, **kwargs)->None:
        """TODO If instance variables are not defined, define environment variables here
        Then add the env variables to my.env for your specific environment variables
        Finally add the variable name and equal sign in a new section in template.env 
        for future use. Extension of __init__
        
        Use self.str_or_env(str | any, str) to prevent accidentally passing int or long as arguments, 
        and also to allow users to define some values
        
        NOTE Try and keep all client errors here, and try and catch as many CredentialErrors
        here by making some api calls here
        NOTE use `__` to make all private information sorta private!!!
        
        Args:
            Add your own and document!
        """   
        self.__token = self.type_or_env(token, "TOKEN") # Example use with a random token
        
    def add_on(self, type_: str="Error")->str:
        """TODO Specify an addon to tack on to the end of each message, solely a cosmetic thing
        If there are big issues with this, ie some platforms are much more annoying I can change 
        this.
        
        Reccomended method, create a classs dict with emojis for "Start", "Stop", and "Error". Use a `.get`
        to return a val but set the default return val one of the 3 emojis.
        Args:
            type_ (function, optional): One of three types of status of the function, "Start", "End", "Error". 
            Helps specify what type of add-on to tack on for personalization, not necessary to implement though!
        """
        return ""        
        
    def send_message(self, MSG: str):
        try:
            """TODO Specify the API and set up of sending a singular message"""
            pass         
        except Exception as ex:
            """Handle the error somewhat or don't. If you want to add more information do it here"""       
            raise ex
