import os
import time
import traceback

from .NotifyMethods import *

# Text Alerts
from twilio.rest import Client

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

    def send_start_MSG(self, func):
        MSG = self.format_message(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime())], type_="Start")
        self.send_MSG_base(MSG)

    def send_end_MSG(self, func, diff): # Used for formatting and sending
        MSG = self.format_message(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime()), diff], type_="End")
        self.send_MSG_base(MSG)

    def send_error_MSG(self, func, ex):
        MSG = self.format_message(formatList=[func.__name__, type(ex), str(ex), time.strftime(DATE_FORMAT, time.localtime()), traceback.format_exc()], type_="Error")+":taraduckface:"
        self.send_MSG_base(MSG)

    def send_message(self, message):
        try:
            self.client.messages.create(to=self.cellphone,
                            from_=self.twilio_number,
                            body=message)
        except Exception as ex:
            raise ex