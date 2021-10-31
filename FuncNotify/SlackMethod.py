from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for [Method].
from slack import WebClient


def time_Slack(func=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, username: str="alerty", token: str=None, email: str=None, *args, **kwargs):
    """Decorator specific for Slack, if no credentials specified, it wil fill in with .env variables
    
    Args:
        func (function, optional): In case you want to use time_func as a pure decoratr without \
        arguments. Defaults to None.
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): Path to .env file. Defaults to ".env".
        update_env (bool, optional): Whether to update the .env file to current. Always updates on \
        initialization. Defaults to False.
        
        username (str, optional): Bot username. Defaults to "alerty".
        token (str, optional): Bot token . Defaults to None.
        email (str, optional): Email of recepient. Defaults to None.
"""
    return time_func(func=func, NotifyMethod="Slack", use_env=use_env, env_path=env_path, update_env=update_env, username=username, email=email, token=token, *args, **kwargs) 


class SlackMethod(NotifyMethods):
    """Sends slack notification to slack channel and user email specified
    """ 
    
    __slots__ = ("__username", "__id", "__client") # List all instance variables here in string form, saves memory
    
    emoji_dict = {
        "Start":    ":clapper:",
        "End":      ":tada:",
        "Error":    ":skull:",
    }   

    def __init__(self, *args, **kwargs):
        """Sets the credentials for the api client for slack

        Args:
            username (str, optional): Bot username. Defaults to "alerty".
            token (str, optional): Bot token . Defaults to None.
            email (str, optional): Email of recepient. Defaults to None.
            
        """    
        super().__init__(*args, **kwargs)
        

    def _set_credentials(self, username: str="alerty", token: str=None, email: str=None,  *args, **kwargs):
        """Sets the credentials for the api client for slack

        Args:
            username (str, optional): Bot username. Defaults to "alerty".
            token (str, optional): Bot token . Defaults to None.
            email (str, optional): Email of recepient. Defaults to None.
            
        """        
        self.__username =  self._type_or_env(username, "USERNAME")
        self.__client = WebClient(self._type_or_env(token, "SLACK_API_TOKEN"))
        
        self.__id = self.__client.users_lookupByEmail(email=self._type_or_env(email, "EMAIL"))['user']['id']
        
        

    def _addon(self, type_: str="Error")->str:
        return SlackMethod.emoji_dict.get(type_, ":tada:")

    def _send_message(self, MSG: str):
        try:
            self.__client.chat_postMessage(username=self.__username, # NOTE this can be any username, 
                                         text=MSG,               # set up the bot credentials!
                                         channel=self.__id)

        except Exception as ex:
            raise ex