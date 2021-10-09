import os
import time
import traceback

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
    
    def __init__(self, environ=None, mute=False, *args, **kwargs):
        self.environ_dict = environ if environ else {}
        NotifyMethods.set_mute(mute)
        
        try:  
            NotifyMethods._logger_init_(self.environ_dict, *args, **kwargs) # Note logger only logs errors in sending the messages, not in the function itself
            
            self._set_credentials(*args, **kwargs)
            self.error=None # Always default to notify user

        except Exception as ex:
            # Consider adding traceback and error here
            NotifyMethods.log(status="ERROR", method=self.__class__.__name__, 
                              message="[CREDENTIALS] Connection to setting up notifications interupted, double check env variables")
            NotifyMethods.log(status="ERROR", method=self.__class__.__name__, 
                              message=f"[CREDENTIALS] {ex}")
            self.error=ex # If error with credentials
        
        NotifyMethods._register(self)
        
    
    def str_or_env(self, val, env_variable: str)->str:
        """Checks if inputted value is string, otherwise searches environment 
        for that variable. If not found, doesn't notify users.s

        Args:
            val ([type]): Input, should always be a string but if not will search environment
            env_variable (str): environment variable name

        Returns:
            str: important information used by apis as a string
        Raises:
            KeyErrorException: Raises if environment variable not found in name, this will set `self.Error` 
            to that exception so it can be accessed
        """             
        return val if isinstance(val, str) else self.environ_dict[env_variable]
    
    @classmethod
    def _register(cls, NotifyObject):
        """Registers each object and creates sa pseudo cyclical buffer that holds 3 objects that
        can be checked when youu grab the registry
        """ 
        if not NotifyObject.error is None:
            NotifyObject=None
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
        if (environ.get("LOG") or log or logger_path) and not cls.logger: # Uses existing logger if it existss
            
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
            file_handler = logging.handlers.RotatingFileHandler(filename="{}/logs/{}.log".format(path, logger_name), 
                                                                maxBytes=int(environ.get("FILE_SIZE", buffer)), 
                                                                backupCount=1)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(logger_file_format))
            cls.logger.addHandler(file_handler)

            # Dictionary houses all logging methdos
            cls.log_method_dict = {"DEBUG": cls.logger.debug,
                                   "INFO" : cls.logger.info,
                                   "WARNING": cls.logger.warning,
                                   "ERROR": cls.logger.error,
                                   "FATAL": cls.logger.fatal,
                                  }
            cls.log_level_dict = {"DEBUG": logging.DEBUG,
                                  "INFO": logging.INFO,
                                  "WARNING": logging.WARNING,
                                  "ERROR": logging.ERROR,
                                  "FATAL": logging.FATAL,
                                 }
        elif not (environ.get("LOG") or log or logger_path):
            cls.logger=None
            


    # Logger suite, functions that control logging functinos that run
    @classmethod
    def set_logger(cls, level: str="DEBUG"):
        cls.logger.setLevel(cls.log_level_dict.get(level, logging.DEBUG))

    @classmethod
    def _format_log(cls, status, method="", message="", *args, **kwargs):
        ret_messsage = "[METHOD={}] Message = {}.".format(method, message) 
        return ret_messsage, {'exc_info': status>logging.INFO} 
    @classmethod
    def log(cls, status: str="DEBUG", *args, **kwargs):
        if cls.logger:
            log_message, kwdict = cls._format_log(cls.log_level_dict.get(status, logging.ERROR), *args, **kwargs)
            cls.log_method_dict.get(status, 
                                    lambda *args, **kwargs: 
                                        [cls.logger.error(*args, **kwargs),
                                         cls.logger.error("Logger method not found, using [ERROR]"),]
                                    )(log_message, **kwdict)
    
    def format_message(self, formatList: list, type_: str="Error"):
        return '\n'.join(NotifyMethods._messageDict[type_]).format(*formatList, machine=socket.gethostname()) + self.addon(type_=type_)
    

    def addon(self, type_: str="Error")->str:
        """Pseudo-abstsract method, sometimess will add emojis and other fun messages
        that are platform specific. Not necessary to implement but you can for personalization!
        """        
        return ""
    
    @abstractmethod
    def _set_credentials(self, *args, **kwargs)->None:
        """Sets up object with environment variables
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

    @abstractmethod
    def send_message(self, message: str)->None: 
        """Interacts with the respective platforms apis, the prior 3 all call this functioon to send the message
        """        
        pass
    
    
    
    def _send_MSG_base(self, *args, **kwargs)->None:
        """All functions begin by calling send_MSG_base and depending on the status of that functioon, it'll be sent or
        an error will be logged if the initial credentials aren't valid

        Args:
            MSG (str): Current MSG to be sent. 
        """ 
        if not NotifyMethods._mute:       
            MSG = self.format_message(*args, **kwargs)
            try:
                if not self.error is None:
                    raise self.error
                
                self.send_message(MSG)
                NotifyMethods.log(status="DEBUG", method=self.__class__.__name__, 
                                  message=MSG)

            except Exception as ex:
                NotifyMethods.log(status="ERROR", method=self.__class__.__name__, 
                                  message=f"[CREDENTIALS] {MSG}")
                self.error = ex
                
              
   
