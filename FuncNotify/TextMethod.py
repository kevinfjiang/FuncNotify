"""Sends text messages to users via a purchased number and twilio

Setup:
    1. Create a twilio accountt and purchase a (free) number. No credit card. Quick guide: https://www.twilio.com/docs/sms/quickstart/python
        1b. Per account, one has limited notifications.
    2. Grab the twilio account, API token, twilio phone and your phone to be added to .env
"""
import FuncNotify.NotifyMethods as NotifyMethods # Using the predefined functions from the abstract class
import FuncNotify.NotifyDecorators as NotifyDecorators

# Specify here other Packages to be imported specific for Text Alerts.
from twilio.rest import Client

def time_Text(func=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, cellphone=None, twiliophone: str=None, twilioaccount: str=None, twiliotoken: str=None, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """Decorator for text alerts, using twilio
    
    Args:
    
        func (function, optional): In case you want to use time_func as a pure decoratr without \
        arguments. Defaults to None.
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): Path to .env file. Defaults to ".env".
        update_env (bool, optional): Whether to update the .env file to current. Always updates on \
        initialization. Defaults to False.
        
        phone (str, optional): your phonenumber. Defaults to None.
        twiliophone (str, optional): twilio specific phone number. Defaults to None.
        twilioaccount (str, optional): twilio account id. Defaults to None.
        twiliotoken (str, optional): twilio specific access token, should all be found \
        in settings tab. Defaults to None.
        """
    return NotifyDecorators.time_func(*args, **kwargs, **locals(), NotifyMethod="Text") 

class TextMethod(NotifyMethods.NotifyMethods):
    """Sends message via twilio if twilio api is set up for text alerts. 
    """  
    
    __slots__ = ("__cellphone", "__twilio_number", "__client") # List all instance variables here in string form, saves memory  

    def __init__(self, *args, **kwargs):
        """Sets credentialls for Twilios

        Args:
            phone (str, optional): your phonenumber. Defaults to None.
            twiliophone (str, optional): twilio specific phone number. Defaults to None.
            twilioaccount (str, optional): twilioo account id. Defaults to None.
            twiliotoken (str, optional): twilio specific access token, should all be found 
            in settings tab. Defaults to None.
        """   
        super().__init__(*args, **kwargs)
        

    def _set_credentials(self, phone: str=None, twiliophone: str=None, twilioaccount: str=None, twiliotoken: str=None, *args, **kwargs):
        """Sets credentialls for Twilios

        Args:
            phone (str, optional): your phonenumber. Defaults to None.
            twiliophone (str, optional): twilio specific phone number. Defaults to None.
            twilioaccount (str, optional): twilioo account id. Defaults to None.
            twiliotoken (str, optional): twilio specific access token, should all be found 
            in settings tab. Defaults to None.
        """        
        self.__cellphone = self._type_or_env(phone, "PHONE")
        self.__twilio_number = self._type_or_env(twiliophone, "TWILIOPHONE")
        self.__client = Client(self._type_or_env(twilioaccount, "TWILIOACCOUNT"), self._type_or_env(twiliotoken, "TWILIOTOKEN"))

    def _send_message(self, message):
        try:
            self.__client.messages.create(to=self.__cellphone,
                                        from_=self.__twilio_number,
                                        body=message)
        except Exception as ex:
            raise ex