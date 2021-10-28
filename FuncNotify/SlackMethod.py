from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for [Method].
from slack import WebClient


def time_Slack(func=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, username: str="alerty", token: str=None, email: str=None, *args, **kwargs):
    """Decorator specific for Slack, if no credentials specified, it wil fill in with .env variables
    
    Args:
        func (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): path to .env file. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updatess on 
        initialization. Defaults to False.
        
        username (str, optional): bot username. Defaults to "alerty".
        token (str, optional): bot token . Defaults to None.
        email (str, optional): email of recepient. Defaults to None.
"""
    return time_func(func=func, NotifyMethod="Slack", use_env=use_env, env_path=env_path, update_env=update_env, username=username, email=email, token=token, *args, **kwargs) 


class SlackMethod(NotifyMethods):
    """Sends slack notification to slack channel and user email specified
    """ 
    
    __slots__ = ("_username", "_id", "_client") # List all instance variables here in string form, saves memory
    
    emoji_dict = {
        "Start":    ":clapper:",
        "End":      ":tada:",
        "Error":    ":skull:",
    }   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def _set_credentials(self, username: str="alerty", token: str=None, email: str=None,  *args, **kwargs):
        """Sets the credentials for the api client for slack

        Args:
            username (str, optional): bot username. Defaults to "alerty".
            token (str, optional): bot token . Defaults to None.
            email (str, optional): email of recepient. Defaults to None.
            
        """        
        self._username =  self.type_or_env(username, "USERNAME")
        self._client = WebClient(self.type_or_env(token, "SLACK_API_TOKEN"))
        
        self._id = self._client.users_lookupByEmail(email=self.type_or_env(email, "EMAIL"))['user']['id']
        
        

    def addon(self, type_: str="Error")->str:
        return SlackMethod.emoji_dict.get(type_, ":tada:")

    def send_message(self, MSG: str):
        try:
            self._client.chat_postMessage(username=self._username, # NOTE this can be any username, 
                                         text=MSG,               # set up the bot credentials!
                                         channel=self._id)

        except Exception as ex:
            raise ex