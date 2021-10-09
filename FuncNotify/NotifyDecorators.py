import time
import warnings
from dotenv import dotenv_values

from .NotifyMethods import *

NOTIFY_TYPE=None
ENV_DICT=None

# Main decorator
def time_func(function=None, NotifyMethod: str="Print", use_env: bool=False, env_path: str=".env", update_env: bool=False, *dec_args, **dec_kwargs): 
    """Decorator for how to handle a notify function. Allows for additional arguments in the decorator
    and support for args like emails/api keys. Is able to handle errors.

    Args:
        function (func, optional): In case you want to use time_func as a decorator without argumetns, 
        NotifyMethod (str, optional): Specifies the type of method used to notify user, selected 
        from NotifyType. Defaults to "Print".
        use_env (str, optional): Loads .env file envionment variables. Defaults to False
        env_path (str, optional): path to .env file. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updatess on 
        initialization. Defaults to False.

        

    Returns:
        function: decorator function for timing
    """    
    
    global NOTIFY_TYPE
    global ENV_DICT
    
    if NOTIFY_TYPE is None:
        NOTIFY_TYPE = NotifyMethods.get_cls_registry()
    if update_env or ENV_DICT is None:
        ENV_DICT={**os.environ, **dotenv_values(env_path)} if use_env else {} 
    
    notify_obj = NOTIFY_TYPE.get(NotifyMethod, default_notify)(environ=ENV_DICT,
                                                                *dec_args, 
                                                                **dec_kwargs)
    
    def time_function(func):
        """Inner wrapped function, used for timing and control

        Args:
            func (function): passes function and arguments down below to the final timer
        """         
        def timer(*func_args, **func_kwargs):
            """Takes arguments from main functioon and passes it down

            Returns:
                Object: returns func's output
            """           
            return timer_base(func, notify_obj, *func_args, **func_kwargs)
        return timer

    if callable(function): # Checks time_func was used as a decorator (@time_func vs @time_func(NotifyMethod="Slack"))
        return time_function(function)

    return time_function


def timer_base(func, NotifyObj: NotifyMethods, *args, **kwargs): 
    """ Timer base, depending on the type of object of NotifyObj, it will notify the 
    user of the methood and time the function.Errors are raised the same method

    Args:
        func (function): Any function
        NotifyObj (NotifyMethods): Object from abstract class that indicates how the user is nootified

    Raises:
        ex (Exception): Any Exception can be excepted then raised, this ensures exceptions aren't 
        interuptted but the user is notified

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

def default_notify(*args, **kwargs):
    warnings.warn(f"Invalid NotifyMethod type specified, will use `PrintMethod`, select a type within this criteria: {NOTIFY_TYPE.keys()}")
    return NOTIFY_TYPE["Print"](args, kwargs)
