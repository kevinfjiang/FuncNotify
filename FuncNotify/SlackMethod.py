from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for [Method].
from slack import WebClient
from random import randint # For random emojis


def time_Slack(function=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, *args, **kwargs):
    """Decorator specific for Slack, if no credentials specified, it wil fill in with .env variables
    
    
    Args:
        function (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): path to .env file. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updatess on 
        initialization. Defaults to False.
"""
    return time_func(function=function, NotifyMethod="Slack", use_env=use_env, env_path=env_path, update_env=update_env, *args, **kwargs) 


class SlackMethod(NotifyMethods):
    """Sends slack notification to slack channel and user email specified
    """    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    def _set_credentials(self, email: str=None, token: str=None, *args, **kwargs):
        self.email = self.str_or_env(email, "EMAIL")
        self.client = WebClient(self.str_or_env(token, "SLACK_API_TOKEN"))
        

    def addon(self, type_: str="Error")->str:
        try:
            emoji_dict = self.client.emoji_list()['emoji']
            rand_emoji = list(emoji_dict.keys())[randint(0, len(emoji_dict))]
            return f":{rand_emoji}:"
        except Exception:
            pass
        finally:
            return ":tada:"
            

    def send_message(self, message: str):
        try:
            self.client.chat_postMessage(username="alerty", # NOTE this can be any username, set up the credentials!
                                        text=message,
                                        channel=self.client.users_lookupByEmail(email=self.email)['user']['id'])

        except Exception as ex:
            raise ex