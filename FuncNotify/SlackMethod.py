import os # Grabbing environment variables

from .NotifyMethods import * # Using the predefined functions from the abstract class

# Specify here other Packages to be imported specific for [Method].
from slack import WebClient
from random import randint # For random emojis


def time_Slack(function=None, dot_env: bool=True, *args, **kwargs):
    """Decorator specific for Slack, if no credentials specified, it wil fill in with .env variables
    
    
    Args:
        function (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        dot_env (bool): Loads .env file envionment variables. Defaults to False"""
    return time_func(function=function, dot_env=dot_env, funcSpecify="Slack",  *args, **kwargs) 


class SlackMethod(NotifyMethods):
    """Sends slack notification to slack channel and user email specified
    """    

    def __init__(self, email: str=None, *args, **kwargs):
        self.email = email
        super(SlackMethod, self).__init__(*args, **kwargs)
        

    def _set_credentials(self):
            slackToken = os.environ["SLACK_API_TOKEN"]
            self.client = WebClient(slackToken)
            
            if self.email is None:
                self.email = os.environ["EMAIL"]

    def addon(self, type_: str=None)->str:
        try:
            emoji_dict = self.client.emoji_list()['emoji']
            rand_emoji = list(emoji_dict.keys())[randint(0, len(emoji_dict))]
            return f":{rand_emoji}:"
        except:
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