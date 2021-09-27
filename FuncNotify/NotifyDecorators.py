import time
import warnings
from dotenv import load_dotenv

from .NotifyMethods import *

NOTIFY_TYPE=None

# Main decorator
def time_func(function=None, use_env=False, env_path=".env", NotifyMethod="Print", *dec_args, **dec_kwargs): 
    """Decorator for how to handle a notify function. Allows for additional arguments in the decorator
    and support for args like emails/api keys. Is able to handle errors.

    Args:
        function (func, optional): In case you want to use time_func as a pure decoratr without argumetns, Alert serves as 
        the function. Defaults to None.
        dot_env (str): Loads .env file envionment variables. Defaults to False
        NotifyMethod (str, optional): Specifies the type of method used to notify user, selected from NotifyType. Defaults to "Print".

    Returns:
        function: decorator function for timing
    """    
    global NOTIFY_TYPE
    
    if NOTIFY_TYPE is None:
        NOTIFY_TYPE = NotifyMethods.get_cls_registry()
    
    if NotifyMethod not in NOTIFY_TYPE:
        warnings.warn("Invalid NotifyMethod type specified, will use `PrintMethod`, select a type within this criteria: {}".format(NotifyType.keys()))
    
    if use_env:
        load_dotenv(env_path)
    else:
        os.environ.clear()
    
    def time_function(func):
        """Inner wrapped function, used for timing and control

        Args:
            func (function): passes function and arguments down beloow to the final timer
        """         
        def timer(*func_args, **func_kwargs):
            """Takes arguments froom main functioon and passes it down

            Returns:
                Object: returns func's output
            """           
            result = timer_base(func, NOTIFY_TYPE.get(NotifyMethod, NOTIFY_TYPE["Print"])(*dec_args, **dec_kwargs), *func_args, **func_kwargs)
            return result
        return timer

    if callable(function): # Checks time_func was used as a decorator(@time_func vs @time_func(NotifyMethod="Slack"))
        func = function
        return time_function(func)

    return time_function


def timer_base(func, NotifyObj, *args, **kwargs): 
    """ Timer base, depending on the type of object of NotifyObj, it will notify the user of the methood and time the function.
    Errors are raised the same method

    Args:
        func (function): Any function
        NotifyObj (NotifyMethods): Object from abstract class that indicates how the user is nootified

    Raises:
        ex (Exception): Any Exception can be excepted then raised, this ensures exceptions aren't interuptted but the user is notified

    Returns:
        Object: Returns whatever the function returns
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
