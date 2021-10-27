import os
import time
import traceback
import inspect

import logging
import logging.handlers

import socket
import collections

from abc import ABCMeta, abstractmethod


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    

class FactoryRegistry(ABCMeta):
    _REGISTRY = {} 
    
    def __new__(cls, clsname, bases, attrs):
        newclass = super(FactoryRegistry, cls).__new__(cls, clsname, bases, attrs)
        if not inspect.isabstract(newclass):  # Removes abstract methods from registry
            cls._REGISTRY[newclass.__name__.replace("Method", "")] = newclass
        return newclass
    
    @classmethod
    def get_cls_registry(cls)->dict:
        return dict(cls._REGISTRY)
    
    
class NotifyMethods(metaclass=FactoryRegistry):
    """Abstract class for the methods of notifying the user, 
    handles the messages and logger for error checking
    """    
    # Tracking and testing, intended to in case one needs to check functions ran
    _registry = collections.deque([], maxlen=5) # Tracks last five for error checking, 
    _mute=False                                 # circular buffer so the garbage collectoor works
    
    __slots__ = ("environ_dict", "error")
    
    logger=None
        
    _messageDict = {"Start": ["Function: {0}() called...",
                              "Machine Name: {machine}",
                              "Start Time: {1}"],
                    
                    "End":   ["Function: {0}() completed",
                              "Machine Name: {machine}",
                              "Finish Time: {1}",
                              "Total Time: {2:.2f}"],
                    
                    "Error": ["Function: {0}() failed due to a {1}",
                              "Exception Reason: \n{2}"
                              "Fail Time Stamp: \n{3}",
                              "Machine Name: {machine}",
                              "Fail Traceback: {4}"]} 
    
    def __init__(self, environ: dict=None, mute: bool=False, use_log: bool=False, *args, **kwargs):
        self.environ_dict = environ if isinstance(environ, dict) else {}
        NotifyMethods.set_mute(mute)
        
        try:  
            NotifyMethods._logger_init_(self.environ_dict, log=use_log, *args, **kwargs) # Note logger only logs errors in sending  
                                                                                         # the messages, not in the function itself
            self._set_credentials(*args, **kwargs)
            self.error=None # Always default to notify user

        except Exception as ex:
            # Consider adding traceback and error here
            NotifyMethods.log(status="ERROR", METHOD=self.__class__.__name__, 
                              message="[CREDENTIALS] Connection to setting up notifications \
                                        interupted, double check env variables")
            NotifyMethods.log(status="ERROR", METHOD=self.__class__.__name__, 
                              message=f"[CREDENTIALS] {ex}") 
            self.error=CredentialError(self, ex) # If error with credentials
        
        NotifyMethods._register(self)
        
    
    def type_or_env(self, val, env_variable: str, type_: type=str)->str:
        """Checks if inputted value is oof the type `type_`, default to string, otherwise 
        searches environment for that variable. If not found, doesn't notify ussers

        Args:
            val (any): Input, should always be a string but if not will search environment
            type_ (type): the type too coompare to 
            env_variable (str): environment variable name

        Returns:
            str or type_: important information used by apis
        Raises:
            KeyError: Raises if environment variable not found in name, this will set `self.Error` 
            to that exception so it can be accessed
        """             
        return val if isinstance(val, type_) else self.environ_dict[env_variable] #TODO Descriptive key error here pls
    
    @classmethod
    def _register(cls, NotifyObject):
        """Registers each object and creates a pseudo cyclical buffer that holds 5 objects that
        can be checked when youu grab the registry
        """ 
        if isinstance(NotifyObject.error, Exception): 
            NotifyObject=NotifyObject.error
        cls._registry.append(NotifyObject)
        
    @classmethod
    def get_registry(cls):
        return cls._registry
    
    @classmethod
    def set_mute(cls, mute: bool=False):
        cls._mute=mute
    

    @classmethod
    def _logger_init_(cls, environ, log: bool=False, buffer: int=65536, logger_path: str=None, *args, **kwargs):
        """Sets up the class logger, should only need to be run once, although if you init it once 
        it'll always be active.

        Args:
            log (bool, optional): [whether to log the files]. Defaults to False.
            debug (bool, optional): [whether to enable debug mode]. Defaults to False.
            buffer (int, optional): [size of each log file]. Defaults to 65536 (2**16).
        """        
        if (environ.get("LOG") or log or logger_path) and cls.logger is None: # Uses existing logger if it existss
            
            if logger_path:
                path=logger_path
            else:
                path = environ.get("LOGGER_PATH", "")
                path = path if path else os.getcwd() # If env variable but not defined is empty sets path to cwd
                
            if not os.path.isdir(os.path.join(path, "logs")):
                os.mkdir("logs")

            import __main__ # Necessary for naming, setting up print formatting
            logger_name = __main__.__file__.split('/')[-1][:-3]

            cls.logger = logging.getLogger(logger_name)
            cls.logger.setLevel(logging.DEBUG)

            logger_console_format = "[%(levelname)s]: %(message)s"
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(logging.Formatter(logger_console_format))
            cls.logger.addHandler(console_handler)

            logger_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"
            file_handler = logging.handlers.RotatingFileHandler(filename=f"{path}/logs/{logger_name}.log",
                                                                maxBytes=int(environ.get("FILE_SIZE", buffer)), 
                                                                backupCount=1)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(logger_file_format))
            cls.logger.addHandler(file_handler)

            # Dictionary houses all logging methods
            logger_strings = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            logger_levels = range(logging.DEBUG, logging.CRITICAL + 1, 10)
            logger_funcs = [cls.logger.debug, cls.logger.info, cls.logger.warning, cls.logger.error, cls.logger.critical]
            
            cls.log_method_dict = dict(zip(logger_strings, logger_funcs))
            cls.log_level_dict = dict(zip(logger_strings, logger_levels))
            
        elif not (environ.get("LOG") or log or logger_path) and environ:
            cls.logger=None
            


    # Logger suite, functions that control logging functinos that run
    @classmethod
    def set_logger(cls, level: int=logging.DEBUG, level_string: str=""):
        if cls.logger is None:
            NotifyMethods._logger_init_(log=True)
        cls.logger.setLevel(cls.log_level_dict.get(level_string, level))
    @classmethod
    def logger_off(cls):
        cls.logger=None
    @classmethod
    def _format_log(cls, status: str, METHOD: str, message: str, *args, **kwargs):
        ret_messsage = f"[{METHOD=}] Message = {message}"
        return ret_messsage, {'exc_info': status>logging.INFO} 
    @classmethod
    def log(cls, status: str="DEBUG", *args, **kwargs):
        if cls.logger:
            log_message, kwdict = cls._format_log(cls.log_level_dict.get(status, logging.ERROR), *args, **kwargs)
            cls.log_method_dict.get(status, 
                                    lambda *args, **kwargs: [
                                        cls.logger.error(*args, **kwargs),
                                        cls.logger.error("Logger method not found, using [ERROR]"),]
                                    )(log_message, **kwdict)
    
    @abstractmethod
    def _set_credentials(self, *args, **kwargs)->None:
        """Sets up object with environment variables
        """        
        pass
    
    @abstractmethod
    def send_message(self, message: str)->None: 
        """Interacts with the respective platforms apis, the prior 3 all call this functioon to send the message
        """        
        pass

    # Suite of funcitons sends and formats messages for each different method. These guys help format each message for each of the instances
    def send_start_MSG(self, func): 
        self._send_MSG_base(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime())], 
                            type_="Start")
    def send_end_MSG(self, func, diff: float): 
        self._send_MSG_base(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime()), diff], 
                            type_="End")
    def send_error_MSG(self, func, ex: Exception): 
        self._send_MSG_base(formatList=[func.__name__, type(ex), str(ex), time.strftime(DATE_FORMAT, time.localtime()), traceback.format_exc()], 
                            type_="Error")
    
    def format_message(self, formatList: list, type_: str="Error"):
        return '\n'.join(NotifyMethods._messageDict[type_]).format(*formatList, machine=socket.gethostname()) + self.addon(type_=type_)
    

    def addon(self, type_: str="Error")->str:
        """Pseudo-abstsract method, sometimess will add emojis and other fun messages
        that are platform specific. Not necessary to implement but you can for personalization!
        """        
        return ""
    
    def _send_MSG_base(self, *args, **kwargs)->None:
        """All functions begin by calling send_MSG_base and depending on the status of that functioon, it'll be sent or
        an error will be logged if the initial credentials aren't valid

        Args:
            MSG (str): Current MSG to be sent. 
        """ 
        MSG = self.format_message(*args, **kwargs)
        if not NotifyMethods._mute:       
            if self.error:
                NotifyMethods.log(status="ERROR", METHOD=self.__class__.__name__, 
                                  message=f"Attempted send of invalid credentials error as follows \n" \
                                          f"[ERROR] {self.error} \n[Message] {MSG}")
                return
            
            try:
                self.send_message(MSG)
                NotifyMethods.log(status="DEBUG", METHOD=self.__class__.__name__, 
                                  message=MSG)

            except Exception as ex:
                self.error=MessageSendError(self, ex)
                NotifyMethods.log(status="ERROR", METHOD=self.__class__.__name__, 
                                  message=f"[Error] {self.error} \n[Message] {MSG}")
        else:
            NotifyMethods.log(status="DEBUG", METHOD=self.__class__.__name__, 
                                  message=f"[Message] {MSG} \n[Muted] True")
                
                
class CredentialError(Exception):
    __slots__=("NotifyObject", "error")
    def __init__(self, NotifyObject: NotifyMethods, error: Exception):
        self.NotifyObject=NotifyObject
        self.error=error 
        super().__init__(self.__str__())
    
    def __str__(self):
        return f"The following exception occurred with the credentials of using {self.NotifyObject.__class__.__name__} \n" \
               f"[Error] {self.error} \n" \
               f"[Fix] Check all credentials are strings and are accurate, check the type hints, and env variables"
        
class MessageSendError(Exception):
    __slots__=("NotifyObject", "error")
    def __init__(self, NotifyObject: NotifyMethods, error: Exception):
        self.NotifyObject=NotifyObject
        self.error=error 
        super().__init__(self.__str__())
    
    def __str__(self):
        return f"The following exception occurred while sening the messagge with the method {self.NotifyObject.__class__.__name__} \n"\
               f"[Error] {self.error} \n" \
               f"[Fix] This is an error with the respective platform's API, ensure the credentials for are valid and you have access," \
               f"check env variables, and ensure that all the types are correct. This is likely an issue with your implementation."
        
        