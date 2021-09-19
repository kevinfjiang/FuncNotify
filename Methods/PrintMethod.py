import time
import traceback

from NotifyMethods import *

class PrintMethod(NotifyMethods):
    """Default print message, only notification is a print in terminal
    """    

    def __init__(self, verbose=True, *args, **kwargs):
        self.V = verbose
        super(PrintMethod, self).__init__(*args, **kwargs)

    def set_credentials(self):
        pass

    def send_start_MSG(self, func):
        MSG = self.format_message(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime())], type_="Start")
        self.send_MSG_base(MSG)

    def send_end_MSG(self, func, diff): # Used for formatting and sending
        MSG = self.format_message(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime()), diff], type_="End")
        self.send_MSG_base(MSG)

    def send_error_MSG(self, func, e):
        MSG = self.format_message(formatList=[func.__name__, type(e), str(e), time.strftime(DATE_FORMAT, time.localtime()),traceback.format_exc()], type_="Error")+":taraduckface:"
        self.send_MSG_base(MSG)
        
    def send_message(self, MSG):
        try:
            if self.V:
                print(MSG)
        except Exception as ex:
            raise ex
