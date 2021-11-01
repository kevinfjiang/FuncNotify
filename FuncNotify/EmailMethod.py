from .NotifyMethods import * # Using the predefined functions from the abstract class
from .NotifyDecorators import time_func

# Specify here other Packages to be imported specific for `Email`. Include why each package is here
import yagmail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def time_Email(func=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, twilio_email: bool=False, sender_email: str=None, subject_line: str=None, sender_password: str=None, target_email: str=None, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """Decorator for sending emails wih yagmail or Sendgrid from twilio
    
    Args:
        func (function, optional): In case you want to use time_func as a pure decoratr without \
        arguments. Defaults to None.
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): Path to .env file. Defaults to ".env".
        update_env (bool, optional): Whether to update the .env file to current. Always updates on \
        initialization. Defaults to False.
        
        sender_email (str, optional): Sender email. Defaults to None.
        sender_passsword (str, optional): Not safe method of using yagmail by passing password in. \
        Reccomend using keyring, see yagmail source. Defaults to None
        target_email (str, optional): Target email. Defaults to None.
        """
    return time_func(func=func, NotifyMethod="Email", use_env=use_env, env_path=env_path, update_env=update_env, twilio_email=twilio_email, subject_line=subject_line, sender_email=sender_email, sender_password=sender_password, target_email=target_email, *args, **kwargs) 

class EmailMethod(NotifyMethods):
    """Sends emails wih yagmail or sendgrid from twilio
    """   
    
    __slots__ = ("__client", "__mail")

    def __init__(self, *args, **kwargs):  
        """Uses yagmail to connect to an gmail aresss and to send emails from there
        Highly reccomend not passing in password and also create a separate email for thi istuation
        Highly reccomen creating an appspecific emailers
        
        Args:
            sender_email (str, optional): Sender email. Defaults to None.
            sender_passsword (str, optional): Not safe method of using yagmail by passing password in. \
            Reccomend using keyring, see yagmail source. Defaults to None
            target_email (str, optional): Target email. Defaults to None.
        """     
        super().__init__(*args, **kwargs)

    def _set_credentials(self, use_gmail: bool=False, subject_line: str=None, sender_email: str=None, sender_password: str=None, sendgrid_api: str=None, target_email: str=None, *args, **kwargs)->None:      
        """Uses yagmail to connect to an gmail aresss and to send emails from there
        Highly reccomend not passing in password and also create a separate email for thi istuation
        Highly reccomen creating an appspecific emailers
        
        Args:
            use_gmail (bool, optional): whether to send using yagmail or sendgrid. Defaults to False.
            subject_line (str, optional): subject line for notifications. Defaults to None.
            sender_email (str, optional): Sender email. Defaults to None.
            sender_passsword (str, optional): Not safe method of using yagmail by passing password in. \
            Reccomend using keyring, see yagmail source. Defaults to None
            sendgrid_api (str, optional): sendgrid api to send messages. Defaults to None.
            target_email (str, optional): Target email. Defaults to None.
        """   
        if subject_line is None:
            import __main__
            subject_line = f"Notifications for { __main__.__file__.split('/')[-1][:-3]}"

        if use_gmail:
            self.__client = yagmail.SMTP(self._type_or_env(sender_email, "SENDER_EMAIL"), 
                                        self._type_or_env(sender_password, "SENDER_PASSWORD") if self._type_or_env(sender_password, "SENDER_PASSWORD") else None)
                
            self.__mail   = {"to":      [self._type_or_env(target_email, "TARGET_EMAIL")], 
                            "subject": self._type_or_env(subject_line, "SUBJECT")}

            
        else:
            self.__client = SendGridAPIClient(self._type_or_env(sendgrid_api, "SENDGRID_API"))
            self.__mail = {"from_email":   self._type_or_env(sender_email, "SENDER_EMAIL"), 
                          "to_emails":    [self._type_or_env(target_email, "TARGET_EMAIL")],
                          "subject":      self._type_or_env(subject_line, "SUBJECT"),}
            
        
     
    def _send_message(self, MSG: str):
        try:
            """Specify the API and set up of sending a singular message"""
            if len(self.__mail)==2:
                _send_mail={**self.__mail, 
                           "contents": MSG}
            else:
                _send_mail={"message": Mail(**self.__mail, html_content=MSG)} # Wrapped for unpacking
                
            self.__client.send(**_send_mail)
        except Exception as ex:
            """Handle the error somewhat or don't. If you want to add more information do it here"""       
            raise ex
