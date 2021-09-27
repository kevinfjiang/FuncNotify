from .NotifyMethods import *
from .NotifyDecorators import time_func

class PrintMethod(NotifyMethods):
    """Default print message, only notification is a print in terminal
    """    

    def __init__(self, verbose: bool=True, *args, **kwargs):
        self.V = verbose
        super().__init__(*args, **kwargs)

    def _set_credentials(self, *args, **kwargs):
        pass
        
    def send_message(self, message: str):
        try:
            if self.V:
                print(message)
        except Exception as ex:
            raise ex
