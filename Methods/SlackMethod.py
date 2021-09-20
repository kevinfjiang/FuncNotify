import os
import time
import traceback

import sys # Version control

from .NotifyMethods import *

# Slack notifications
if sys.version_info < (3,0): 
    from slackclient import SlackClient
else:
    from slack import WebClient

class SlackMethod(NotifyMethods):
    """Sends slack notification to slack channel and user email specified
    """    

    def __init__(self, email=None, *args, **kwargs):
        self.email = email
        super(SlackMethod, self).__init__(*args, **kwargs)
        

    def _set_credentials(self):
            slackToken = os.environ["SLACK_API_TOKEN"]
            if sys.version_info < (3,0): # Different versions have different properties of establishing the client
                self.client = SlackClient(slackToken)
            else:
                self.client = WebClient(token=slackToken)
            
            if self.email is None:
                self.email = os.environ["EMAIL"]

    def send_start_MSG(self, func):
        MSG = self.format_message(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime())], type_="Start") + ":party_blob:" # Default emoji
        self.send_MSG_base(MSG)

    def send_end_MSG(self, func, diff): # Used for formatting and sending
        MSG = self.format_message(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime()), diff], type_="End") + ":tada:"
        self.send_MSG_base(MSG)

    def send_error_MSG(self, func, e):
        MSG = self.format_message(formatList=[func.__name__, type(e), str(e), time.strftime(DATE_FORMAT, time.localtime()), traceback.format_exc()], type_="Error") + ":taraduckface:"
        self.send_MSG_base(MSG)

    def send_message(self, message):
        try:
            if sys.version_info < (3,0): # Different versions have different functions
                self.client.api_call("chat.postMessage",
                                    username="alerty",
                                    channel=self.client.api_call(
                                                                "users.lookupByEmail",
                                                                email=self.email)['user']['id'],
                                    text=message)     
            else:
                response = self.client.chat_postMessage(username="alerty", # NOTE this can be any username, set up the credentials!
                                                    text=message,
                                                    channel=self.client.users_lookupByEmail(email=self.email)['user']['id'])

        except Exception as ex:
            raise ex