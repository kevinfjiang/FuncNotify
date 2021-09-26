import os # Grabbing environment variables

from .NotifyMethods import * # Using the predefined functions from the abstract class

# Specify here other Packages to be imported specific for Text Alerts.
from twilio.rest import Client

def time_Text(function=None, dot_env=True, cellphone=None, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """Decorator specific for text, if no credentials specified, it wil fill in with .env variables
    
    Args:
        function (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        dot_env (bool, optional): Loads .env file envionment variables. Defaults to False
        cellphone ([type], optional): [description]. Defaults to None."""
    return time_func(function=function, dot_env=dot_env, cellphone=cellphone, funcSpecify="Text", *args, **kwargs) 

class TextMethod(NotifyMethods):
    """Sends message via twilio if twilio api is set up for text alerts. If a twilio emplooyee reads this, HELLO!
    """    

    def __init__(self, cellphone=None, *args, **kwargs):
        self.cellphone = cellphone
        super(TextMethod, self).__init__(args, kwargs)
        

    def _set_credentials(self):
        if self.cellphone is None:
            self.cellphone = os.environ["PHONE"]
        self.twilio_number = os.environ["TWILIOPHONE"]
        self.client = Client(os.environ["TWILIOACCOUNT"], os.environ["TWILIOTOKEN"])

    def send_message(self, message):
        try:
            self.client.messages.create(to=self.cellphone,
                            from_=self.twilio_number,
                            body=message)
        except Exception as ex:
            raise ex