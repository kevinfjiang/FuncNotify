import time
import warnings
from dotenv import load_dotenv

from funcNotify.Methods import *

# Dictionary to instatiate the objects that define the method which the user is notified
NotifyType = {"Print": PrintMethod, # TODO autoomate import and creation of these methoods, shouldn't be hard?
              "Slack": SlackMethod, 
              "Text": TextMethod, # TODO add more methods eventually. Think of a better way to automate this
             } 

def timer_base(func, NotifyObj, *args, **kwargs): 
    """ Timer base, depending on the type of object of NotifyObj, it will notify the user of the methood and time the function.
    Errors are raised the same method

    Args:
        func (function): Any function
        NotifyObj (NotifyMethods): Object from abstract class that indicates how the user is nootified

    Raises:
        ex (Exception): Any Exception can be excepted then raised, this ensures exceptions aren't interuptted but the user is notified

    Returns:
        [Object]: Returns whatever the functiono returns
    """    
    try:
        NotifyObj.send_start_MSG(func)
        start=time.time()

        result = func(*args, **kwargs)
        
        end=time.time()
        NotifyObj.send_end_MSG(func, end-start)
    
    except Exception as ex: 
        NotifyObj.send_error_MSG(func, ex)
        raise ex

    return result

# Main decorator
def time_func(function=None, dot_env=False, env_path=None, NotifyMethod="Print", *dec_args, **dec_kwargs): # Include support for slack and also include error checking/handeling
    """Decorator for how to handle a notify function. Allows for additional arguments in the decorator
    and support for args like emails/api keys

    Args:
        function (func, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        dot_env (bool): Loads .env file envionment variables. Defaults to False
        funcSpecify (str, optional): Specifies the type of method used to notify user, selected from NotifyType.  
        Defaults to "Print".

    Returns:
        function: decorator functioono for timing
    """    
    if NotifyMethod not in NotifyType:
        warnings.warn("Invalid NotifyMethod type specified, will use PrintMethod, select a type within this criteria: {}".format(NotifyType.keys()))
    
    if dot_env:
        load_dotenv(dotenv_path=env_path)
    
    def time_function(func):
        """Inner wrapped function, used for timing and control

        Args:
            func (function): passes function and arguments down beloow to the final timer
        """         
        def timer(*func_args, **func_kwargs):
            """Takes arguments froom main functioon and passes it down

            Returns:
                [Object]: returns func's output
            """           
            result = timer_base(func, NotifyType.get(NotifyMethod, PrintMethod)(*dec_args, **dec_kwargs), *func_args, **func_kwargs)
            return result
        return timer

    if callable(function): # Checks if Alert is actually a function and time_func was used as a decoratoor(@time_func vs @time_func(funcSpecify="Slack"))
        func = function
        return time_function(func)

    return time_function

def time_text(function=None, dot_env=False, *args, **kwargs): # Include something to check the rest of the arguments in the word
    """Args:
        function (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        dot_env (bool): Loads .env file envionment variables. Defaults to False"""
    return time_func(function=function, dot_env=dot_env, funcSpecify="Text", *args, **kwargs) 
    
def time_slack(function=None, dot_env=False, *args, **kwargs):
    """Args:
        function (function, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        dot_env (bool): Loads .env file envionment variables. Defaults to False"""
    return time_func(function=function, dot_env=dot_env, funcSpecify="Slack",  *args, **kwargs) 

    

