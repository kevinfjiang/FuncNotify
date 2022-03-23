import os
import time
import warnings
import collections

import FuncNotify

import dotenv

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
        collections.deque(map(lambda NotifyObj: NotifyObj.send_start_MSG(func), NotifyObjList), maxlen=0) # sends message on each item in list
        start = time.perf_counter()                                                                   # by iterating through the map
        
        result = func(*args, **kwargs)
        
        diff = time.perf_counter()-start
        collections.deque(map(lambda NotifyObj: NotifyObj.send_end_MSG(func, diff), NotifyObjList), maxlen=0)
    except Exception as ex: 
        collections.deque(map(lambda NotifyObj: NotifyObj.send_error_MSG(func, ex), NotifyObjList), maxlen=0) # noqa: F821 Bizarre bug with flake8, opening an issue
        raise ex

    return result


def get_notify_obj(NotifyMethod: str, environ_dict: dict, obj_args, obj_kwargs, target_dict: dict=None):
    """Creates the object and returns it's a function for reusability

    Args:
        NotifyMethod (str): String deciding what the notify type is
        environ_dict (dict): environment variables dictionary
        obj_args (tuple): notify object tuple arguments
        obj_kwargs (dict): notify object dictionary key ward arguments
        target_dict (dict, optional): Specific arguments specified for a user. Defaults to None.

    Returns:
        NotifyMethods: NotifyMethods obbject that allows you to send start, stop and error messages
    """
    def default_notify(*args, **kwargs): # Sends a warning your notify method didn't match 
        warnings.warn(f"Invalid NotifyMethod type '{NotifyMethod}' specified, will use `PrintMethod`, " \
                      f"select a type within these keys: {[key for key in FuncNotify.NotifyTypes]}.")
        return FuncNotify.NotifyTypes["Print"](*args, **kwargs)
    
    if target_dict is None:
        target_dict={}

    return FuncNotify.NotifyTypes.get(NotifyMethod, default_notify)(environ=environ_dict,
                                                                    *obj_args, 
                                                                    **target_dict,
                                                                    **obj_kwargs)
                

def Notify_Obj_Factory(NotifyMethod: str=None, use_env: bool=True, env_path: str=".env", update_env: bool=False, 
              multi_target: list=None, multi_env: list=None, func=None, message: str=None, args=None, kwargs=None)-> list: 
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
        ENV_DICT={**os.environ, **dotenv.dotenv_values(env_path)} if use_env else {} 
    
    if multi_env and multi_target: 
        # NOTE multi_target and multi_env must be corresponding and will only do up shortest of the two lissts
        for target, spec_env_path in zip(multi_target, multi_env):
            spec_environ_dict={**ENV_DICT, **dotenv.dotenv_values(spec_env_path)} if spec_env_path else ENV_DICT
            target_method=target.get("NotifyMethod", NotifyMethod)
            method_string=target_method if target_method else spec_environ_dict.get("DEFAULTNOTIFY", "NotFound")
            
            notify_obj_list.append(
                get_notify_obj(method_string,
                               target_dict=target, environ_dict=spec_environ_dict, 
                               obj_args=args, obj_kwargs=kwargs))
    elif multi_target:
        for target in multi_target: # Rewrite as a function for easier reuse
            notify_obj_list.append(
                get_notify_obj(NotifyMethod=target.get("NotifyMethod", NotifyMethod),
                               target_dict=target, environ_dict=ENV_DICT, 
                               obj_args=args, obj_kwargs=kwargs))
    elif multi_env:
         for spec_env_path in multi_env:
            spec_environ_dict={**ENV_DICT, **dotenv.dotenv_values(spec_env_path)}
            notify_obj_list.append(
                get_notify_obj(NotifyMethod=NotifyMethod if NotifyMethod else spec_environ_dict.get("DEFAULTNOTIFY", "NotFound"), 
                               environ_dict=spec_environ_dict, obj_args=args, obj_kwargs=kwargs))
    else:
        notify_obj_list.append(
            get_notify_obj(NotifyMethod=NotifyMethod if NotifyMethod else ENV_DICT.get("DEFAULTNOTIFY", "NotFound"), 
                           environ_dict=ENV_DICT, obj_args=args, obj_kwargs=kwargs))
    
    return notify_obj_list
