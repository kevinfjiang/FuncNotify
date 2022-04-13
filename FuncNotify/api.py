"""Main decoratory for FuncNotify with all env variables

To use, use @time_func as a decorator or pass arguments to @time_func(*args, **kwargs) as a decorator
"""
import FuncNotify._timer as _timer
from FuncNotify.NotifyMethods import NotifyMethods

ENV_DICT = None

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
    NotifyObjList = _timer.Notify_Obj_Factory(**locals())

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
            return _timer.timer_base(func_inner, NotifyObjList, *func_args, **func_kwargs)
        return timer     
        
    if callable(func): # Checks time_func was used as a decorator (@time_func vs @time_func(NotifyMethod="Slack"))
        return time_function(func)

    return time_function


 
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
    for NOF in _timer.Notify_Obj_Factory(**locals()):
        NOF.send_custom_MSG(message)
    
