from .NotifyMethods import *

class PrintMethod(NotifyMethods):
    """Default print message, only notification is a print in terminal
    """    

    def __init__(self, verbose: bool=True, *args, **kwargs):
        self.V = verbose
        super(PrintMethod, self).__init__(*args, **kwargs)

    def _set_credentials(self):
        pass
        
    def send_message(self, message: str):
        try:
            if self.V:
                print(message)
        except Exception as ex:
            raise ex
