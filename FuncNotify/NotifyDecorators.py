import time
import warnings
from collections import deque
from dotenv import dotenv_values

from .NotifyMethods import *

NOTIFY_TYPE=None
ENV_DICT=None

# Main decorator TODO maybe, do i force static typing?
def time_func(func=None, NotifyMethod: str=None, use_env: bool=False, env_path: str=".env", update_env: bool=False, 
              multi_target: list=None, multi_env: list=None, *dec_args, **dec_kwargs): 
    """Decorator for how to handle a notify function. Allows for additional arguments in the decorator
    and support for args like emails/api keys. Is able to handle errors.

    Args:
        func (function, optional): In case you want to use time_func as a decorator without argumetns, 
        NotifyMethod (str, optional): Specifies the type of method used to notify user, selected 
        from NotifyType. Defaults to None.
        use_env (str, optional): Whether to load the current env+the env_path. Defaults to False
        env_path (str, optional): path to .env file. Input "" for just the current environment. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updates on 
        initialization. Defaults to False.
        
        multi_target (list[dict], optional): A list of dictionary of keyword arguments for every new target. Defaults to ".env".
        multi_env (list[str], optional): list of strings of paths to `env` files. If you use multi_target and multi_env in
        conjunction you can create a correspondence of new targets with specific .env files to notify. Defaults ot None.

        use_log(bool, optional): Whether to log the output, defaults to True
        

    Returns:
        function: decorator function for timing
    """    
    notify_obj_list=[]
    
    global NOTIFY_TYPE
    global ENV_DICT
    
    if NOTIFY_TYPE is None:
        NOTIFY_TYPE = NotifyMethods.get_cls_registry()
    
    if update_env or ENV_DICT is None or not use_env:
        ENV_DICT={**os.environ, **dotenv_values(env_path)} if use_env else {} 
        
    if multi_env and multi_target: 
        # NOTE multi_target and multi_env must be corresponding and will only do up shortest of the two lissts
        for target, spec_env_path in zip(multi_target, multi_env):
            spec_environ_dict={**ENV_DICT, **dotenv_values(spec_env_path)} if spec_env_path else ENV_DICT
            target_method=target.get("NotifyMethod", NotifyMethod)
            method_string=target_method if target_method else spec_environ_dict.get("DEFAULTNOTIFY", "NotFound")
            
            notify_obj_list.append(
                get_notify_obj(method_string,
                               target_dict=target, environ_dict=spec_environ_dict, 
                               obj_args=dec_args, obj_kwargs=dec_kwargs))
    elif multi_target:
        for target in multi_target: # Rewrite as a function for easier reuse
            notify_obj_list.append(
                get_notify_obj(Notif=target.get("NotifyMethod", NotifyMethod),
                               target_dict=target, environ_dict=ENV_DICT, 
                               obj_args=dec_args, obj_kwargs=dec_kwargs))
    elif multi_env:
         for spec_env_path in multi_env:
            spec_environ_dict={**ENV_DICT, **dotenv_values(spec_env_path)}
            notify_obj_list.append(
                get_notify_obj(Notif=NotifyMethod if NotifyMethod else spec_environ_dict.get("DEFAULTNOTIFY", "NotFound"), 
                               environ_dict=spec_environ_dict, obj_args=dec_args, obj_kwargs=dec_kwargs))
    else:
        notify_obj_list.append(
            get_notify_obj(Notif=NotifyMethod if NotifyMethod else ENV_DICT.get("DEFAULTNOTIFY", "NotFound"), 
                           environ_dict=ENV_DICT, obj_args=dec_args, obj_kwargs=dec_kwargs))
    
    def time_function(func_inner):
        """Inner wrapped function, used for timing and control, necessary to give the
        decorator additional arguments that can be passed in

        Args:
            func_inner (function): passes function and arguments down below to the final timer
        """         
        def timer(*func_args, **func_kwargs):
            """Takes arguments from main function and passes it down

            Returns:
                Object: returns func's output
            """           
            return timer_base(func_inner, notify_obj_list, *func_args, **func_kwargs)
        return timer

    if callable(func): # Checks time_func was used as a decorator (@time_func vs @time_func(NotifyMethod="Slack"))
        return time_function(func)

    return time_function


def timer_base(func, NotifyObjList: list, *args, **kwargs): 
    """ Timer base, depending on the type of object of NotifyObj, it will notify the 
    user of the method and time the function. Errors are raised in the same method
    Leverages a factory that created the object and utilizes the abstract methods

    Args:
        func (function): Any function
        NotifyObjList (list[NotifyMethods]): Object from abstract class that indicates how the user is nootified

    Raises:
        ex (Exception): Any Exception can be excepted then raised, this ensures exceptions aren't 
        interuptted but the user is notified

    Returns:
        Object: Returns whatever the function returns
    """    
    try:
        deque(map(lambda NotifyObj: NotifyObj.send_start_MSG(func), NotifyObjList), maxlen=0) # sends message on each item in list
        start = time.time()                                                                   # by iterating through the map
        
        result = func(*args, **kwargs)
        
        end = time.time()
        deque(map(lambda NotifyObj: NotifyObj.send_end_MSG(func, end-start), NotifyObjList), maxlen=0)
    
    except Exception as ex: 
        deque(map(lambda NotifyObj: NotifyObj.send_error_MSG(func, ex), NotifyObjList), maxlen=0)
        raise ex

    return result

def get_notify_obj(Notif: str, environ_dict: dict, obj_args, obj_kwargs, target_dict: dict=None):
    """Creates the object and returns it's a function for reusability

    Args:
        Notif (str): String deciding what the notify type is
        environ_dict (dict): environment variables dictionary
        obj_args (tuple): notify object tuple arguments
        obj_kwargs (dict): notify object dictionary key ward arguments
        target_dict (dict, optional): Specific arguments specified for a user. Defaults to None.

    Returns:
        NotifyObj: NotifyObject that allows you to send start, stop and error messages
    """
    
    def default_notify(*args, **kwargs): # Sends a warning your notify method didn't match 
        warnings.warn(f"Invalid NotifyMethod type '{Notif}' specified, will use `PrintMethod`," \
                      f"select a type within this criteria: {NOTIFY_TYPE.keys()}")
        return NOTIFY_TYPE["Print"](*args, **kwargs)
    
    if target_dict is None:
        target_dict={}
        
    return NOTIFY_TYPE.get(Notif, default_notify)(environ=environ_dict,
                                                 *obj_args, 
                                                 **target_dict,
                                                 **obj_kwargs)
    

