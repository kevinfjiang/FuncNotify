from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for `Email`. Include why each package is here

def time_Email(func=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """TODO Decorator specific for Email, if no credentials specified, it wil fill in with .env variables. 
    
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
    return time_func(func=func, NotifyMethod="Email", use_env=use_env, env_path=env_path, update_env=update_env, *args, **kwargs) 

class EmailMethod(NotifyMethods):
    """Summaraize exactly how this EmailMethod will notify the end user and what platform.
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
        
        Use self.str_or_env(str | any, str) to prevent accidentally passing int or long as arguments, 
        and also to allow users to define some values
        
        NOTE/TODO one day i plan to add multi notification support, it would probably be done
        here with an additional layer in the str_or_env variable to allow lists of people to be notified
        
        Args:
            Add your own and document!
        """   
        self.token = self.str_or_env(token, "TOKEN") # Example use with a random token
        
    def add_on(self, type_: str="Error")->str:
        """Specify an addon to tack on to the end of each message, solely a cosmetic thing
        If there are big issues with this, ie some platforms are much more annoying I can change 
        this 
        Args:
            type_ (function, optional): One of three types of status of the function, "Start", "End", "Error". 
            Helps specify what type of add-on to tack on for personalization, not necessary to implement though!
        """
        return ""        
        
    def send_message(self, MSG: str):
        try:
            """Specify the API and set up of sending a singular message"""
            pass         
        except Exception as ex:
            """Handle the error somewhat or don't. If you want to add more information do it here"""       
            raise ex
