"""Main decoratory for FuncNotify with all env variables

To use, use @time_func as a decorator or pass arguments to @time_func(*args, **kwargs) as a decorator
"""
import time
import os
import warnings
from collections import deque
from dotenv import dotenv_values

import FuncNotify

ENV_DICT=None

# Main decorator
def time_func(func=None, NotifyMethod: str=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, 
              multi_target: list=None, multi_env: list=None, *args, **kwargs): 
    """Decorator for how to handle a notify function. Allows for additional arguments in the decorator
    and support for args like emails/api keys. Is able to handle errors.

    Args:
        func (function, optional): In case you want to use time_func as a decorator without argumetns, 
        NotifyMethod (str, optional): Specifies the type of method used to notify user, selected \
        from FuncNotify.NotifyTypes. Defaults to None.
        use_env (str, optional): Whether to load the current env+the env_path. Defaults to True
        env_path (str, optional): path to .env file. Input "" for just the current environment. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updates on 
        initialization. Defaults to False.
        
        multi_target (list[dict], optional): A list of dictionary of keyword arguments for every new target. Defaults to ".env".
        multi_env (list[str], optional): list of strings of paths to `env` files. If you use multi_target and multi_env in
        conjunction you can create a correspondence of new targets with specific .env files to notify. Defaults ot None.

        

    Returns:
        function: decorator function for timing
    """    
    NotifyObjList=Notify_Obj_Factory(**locals())

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
            return timer_base(func_inner, NotifyObjList, *func_args, **func_kwargs)
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
        NotifyObjList (list[NotifyMethods]): Object from abstract class that indicates how the user is notified

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
        deque(map(lambda NotifyObj: NotifyObj.send_error_MSG(func, ex), NotifyObjList), maxlen=0) # noqa: F821 Bizarre bug with flake8, opening an issue
        raise ex

    return result

def Notify_Obj_Factory(NotifyMethod: str=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, 
              multi_target: list=None, multi_env: list=None, func=None, message: str=None, verbose=None, args=None, kwargs=None)-> list: 
    """Creates a list of NotifyMethods Objects to be used to send messages

    Args:
        func (function, optional): In case you want to use time_func as a decorator without argumetns, 
        NotifyMethod (str, optional): Specifies the type of method used to notify user, selected \
        from FuncNotify.NotifyTypes. Defaults to None.
        use_env (str, optional): Whether to load the current env+the env_path. Defaults to True
        env_path (str, optional): path to .env file. Input "" for just the current environment. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updates on 
        initialization. Defaults to False.
        
        multi_target (list[dict], optional): A list of dictionary of keyword arguments for every new target. Defaults to ".env".
        multi_env (list[str], optional): list of strings of paths to `env` files. If you use multi_target and multi_env in
        conjunction you can create a correspondence of new targets with specific .env files to notify. Defaults ot None.

        message(bool, optional): Used for message notifications
        

    Returns:
        list: List of NotifyMethods Objects to be used to send messages with
    """    
    
    notify_obj_list=[]
    global ENV_DICT
    
    if update_env or ENV_DICT is None or not use_env:
        ENV_DICT={**os.environ, **dotenv_values(env_path)} if use_env else {} 
    
    if multi_env and multi_target: 
        # NOTE multi_target and multi_env must be corresponding and will only do up shortest of the two lissts
        for target, spec_env_path in zip(multi_target, multi_env):
            spec_environ_dict={**ENV_DICT, **dotenv_values(spec_env_path)} if spec_env_path else ENV_DICT
            target_method=target.get("NotifyMethod", NotifyMethod)
            method_string=target_method if target_method else spec_environ_dict.get("DEFAULTNOTIFY", "NotFound")
            
            notify_obj_list.append(
                Get_notify_obj(method_string,
                               target_dict=target, environ_dict=spec_environ_dict, 
                               obj_args=args, obj_kwargs=kwargs))
    elif multi_target:
        for target in multi_target: # Rewrite as a function for easier reuse
            notify_obj_list.append(
                Get_notify_obj(Notif=target.get("NotifyMethod", NotifyMethod),
                               target_dict=target, environ_dict=ENV_DICT, 
                               obj_args=args, obj_kwargs=kwargs))
    elif multi_env:
         for spec_env_path in multi_env:
            spec_environ_dict={**ENV_DICT, **dotenv_values(spec_env_path)}
            notify_obj_list.append(
                Get_notify_obj(Notif=NotifyMethod if NotifyMethod else spec_environ_dict.get("DEFAULTNOTIFY", "NotFound"), 
                               environ_dict=spec_environ_dict, obj_args=args, obj_kwargs=kwargs))
    else:
        notify_obj_list.append(
            Get_notify_obj(Notif=NotifyMethod if NotifyMethod else ENV_DICT.get("DEFAULTNOTIFY", "NotFound"), 
                           environ_dict=ENV_DICT, obj_args=args, obj_kwargs=kwargs))
    
    return notify_obj_list

def Get_notify_obj(Notif: str, environ_dict: dict, obj_args, obj_kwargs, target_dict: dict=None):
    """Creates the object and returns it's a function for reusability

    Args:
        Notif (str): String deciding what the notify type is
        environ_dict (dict): environment variables dictionary
        obj_args (tuple): notify object tuple arguments
        obj_kwargs (dict): notify object dictionary key ward arguments
        target_dict (dict, optional): Specific arguments specified for a user. Defaults to None.

    Returns:
        NotifyMethods: NotifyMethods obbject that allows you to send start, stop and error messages
    """
    print(obj_kwargs)
    def default_notify(*args, **kwargs): # Sends a warning your notify method didn't match 
        warnings.warn(f"Invalid NotifyMethod type '{Notif}' specified, will use `PrintMethod`, " \
                      f"select a type within these keys: {[key for key in FuncNotify.NotifyTypes]}.")
        return FuncNotify.NotifyTypes["Print"](*args, **kwargs)
    
    if target_dict is None:
        target_dict={}
        
    return FuncNotify.NotifyTypes.get(Notif, default_notify)(environ=environ_dict,
                                                            *obj_args, 
                                                            **target_dict,
                                                            **obj_kwargs)
                
 
def custom_message(message: str, NotifyMethod: str=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, 
                   multi_target: list=None, multi_env: list=None, *args, **kwargs): 
    """Sends custom messages for the multiple targets in .env or specified, utilizes  the same code as time_func to send
    the custom messages which is nice

    Args:
        message (str): Message to be send to everybody
        NotifyMethod (str, optional): Specifies the type of method used to notify user, selected \
        from NotifyType. Defaults to None.
        use_env (str, optional): Whether to load the current env+the env_path. Defaults to True
        env_path (str, optional): path to .env file. Input "" for just the current environment. Defaults to ".env".
        update_env (bool, optional): whether to update the .env file to current. Always updates on 
        initialization. Defaults to False.
        
        multi_target (list[dict], optional): A list of dictionary of keyword arguments for every new target. Defaults to ".env".
        multi_env (list[str], optional): list of strings of paths to `env` files. If you use multi_target and multi_env in \
        conjunction you can create a correspondence of new targets with specific .env files to notify. Defaults ot None.
        

    Returns:
        function: decorator function for timing
    """    
    NotifyObjList=Notify_Obj_Factory(**locals())
        
    deque(map(lambda NotifyObj: NotifyObj.send_custom_MSG(message), NotifyObjList), maxlen=0)
    
