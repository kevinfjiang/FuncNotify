from . import NotifyMethods # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for Text Alerts.
from twilio.rest import Client

def time_Text(function=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, cellphone=None, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """Decorator specific for text, if no credentials specified, it wil fill in with .env variables
    
    Args:
        function (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        use_env (bool, optional): Loads .env file envionment variables. Defaults to False
        cellphone ([type], optional): [description]. Defaults to None."""
    return time_func(function=function, NotifyMethod="Text", use_env=use_env, env_path=env_path, update_env=update_env, cellphone=cellphone, *args, **kwargs) 

class TextMethod(NotifyMethods):
    """Sends message via twilio if twilio api is set up for text alerts. If a twilio emplooyee reads this, HELLO!
    """    

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        

    def _set_credentials(self, phone: str=None, twiliophone: str=None, twilioaccount: str=None, twiliotoken: str=None, *args, **kwargs):
        self.cellphone = self.str_or_env(phone, "PHONE")
        self.twilio_number = self.str_or_env(twiliophone, "TWILIOPHONE")
        self.client = Client(self.str_or_env(twilioaccount, "TWILIOACCOUNT"), self.str_or_env(twiliotoken, "TWILIOTOKEN"))

    def send_message(self, message):
        try:
            self.client.messages.create(to=self.cellphone,
                            from_=self.twilio_number,
                            body=message)
        except Exception as ex:
            raise ex