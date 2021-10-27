from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for `Email`. Include why each package is here
import yagmail

def time_Email(func=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, sender_email: str=None, sender_password: str=None, target_email: str=None, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """TODO Decorator specific for Email, if no credentials specified, it wil fill in with .env variables. 
    
    Args:
        func (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): path to .env file. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updatess on 
        initialization. Defaults to False.
        
        sender_email (str, optional): your email. Defaults to None.
        sender_passsword (str, pls don't use this, not safe). Defaultss to None
        target_email (str, optional): target email. Defaults to None.
        
        Insert remaining args here
        NOTE add all key word arguments that could be used by the class to enable more accurate mesaging
        [variable] ([type], optional): [Summary]. Defaults to [Default]"""
    return time_func(func=func, NotifyMethod="Email", use_env=use_env, env_path=env_path, update_env=update_env, sender_email=sender_email, sender_password=sender_password, target_email=target_email, *args, **kwargs) 

class EmailMethod(NotifyMethods):
    """Sends emails wih yagmail
    """   
    
    __slots__ = ("email")

    def __init__(self, *args, **kwargs):
        """Specify key word arguments in the init as var=xyz and define them as instances
        """        
        super().__init__(*args, **kwargs)

    def _set_credentials(self, sender_email: str=None, sender_password: str=None, target_email: str=None, *args, **kwargs)->None:
        """Uses yagmail to connect to an gmail aresss and to send emails from there
        Highly reccomend not passing in password and also create a separate email for thi istuation
        Highly reccomen creating an appspecific emailers
        Args:
            sender_email (str, optional): your email. Defaults to None.
            sender_passsword (str, pls don't use this, not safe). Defaultss to None
            target_email (str, optional): target email. Defaults to None.
        """   
        self.yag_client =    
        
    def send_message(self, MSG: str):
        try:
            """Specify the API and set up of sending a singular message"""
            pass         
        except Exception as ex:
            """Handle the error somewhat or don't. If you want to add more information do it here"""       
            raise ex
