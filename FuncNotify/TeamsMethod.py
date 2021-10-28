from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for `Teams`. Include why each package is here
import json
import requests

def time_Teams(func=None, use_env: bool=True, env_path: str=".env", update_env: bool=False,  username: str=None, webhook_url: str=None, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """Decorator specifically for microsoft teams

    Args:
        func (function, optional): In case you want to use time_func as a pure decoratr without argumetns. Defaults to None.
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): path to .env file. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updatess on 
        initialization. Defaults to False.
        
        username (str, optional): username of the message bot Defaults to None.
        webhook_url (str, optional): url for the teams channel. Defaults to None.
    """    
    return time_func(func=func, NotifyMethod="Teams", use_env=use_env, env_path=env_path, update_env=update_env,  username=username, webhook_url=webhook_url,*args, **kwargs) 

class TeamsMethod(NotifyMethods):
    """Sends a posted message to the webhook url from the specified username. Uses standard get and post requests.
    Inspiredd by knocknock
    """    
    
    __slots__ = ("_webhook_url", "_dump") # List all instance variables here in string form, saves memory
    
    emoji_dict = {
        "Start":    ":clapper:",
        "End":      ":tada:",
        "Error":    ":skull:",
    }

    def __init__(self, *args, **kwargs):
        """Specify key word arguments in the init as var=xyz and define them as instances
        """        
        super().__init__(*args, **kwargs)

    def _set_credentials(self, username: str=None, webhook_url: str=None, *args, **kwargs)->None:
        """Setting the credentials

        Args:
            username (str, optional): username of the message bot Defaults to None.
            webhook_url (str, optional): url for the teams channel. Defaults to None.
        """        
        self._webhook_url = self.type_or_env(webhook_url, "WEBHOOK")
        
        self._dump = { # Creates json dump with the credentials, more is added laters
            "username": self.type_or_env(username, "USERNAME"),
            "icon_emoji": ":clapper:",
        }
        
    def add_on(self, type_: str="Error")->str:
        """Adds on emoji and tacks on to icon_emoji
        Args:
            type_ (function, optional): One of three types of status of the function, "Start", "End", "Error". 
            Helps specify what type of add-on to tack on for personalization, not necessary to implement though!
        """
        self._dump['icon_emoji'] = TeamsMethod.emoji_dict.get(type_, ":tada:") # Sets clapper as icon without returning val
        
        return ""        
        
    def send_message(self, MSG: str):
        try:
            """Specify the API and set up of sending a singular message"""
            self._dump['text'] = MSG
            requests.post(self._webhook_url, json.dump(self._dump)) # Posts the message
        except Exception as ex:
            """Handle the error somewhat or don't. If you want to add more information do it here"""       
            raise ex
