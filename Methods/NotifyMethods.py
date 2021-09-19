import os

import logging
import logging.handlers
import collections

import socket

from abc import ABCMeta, abstractmethod

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class NotifyMethods:
    """Abstract method for the methods of notifying the user
    """    
    
    __metaclass__ = ABCMeta   

    # Tracking and testing, intended to in case one needs to check functions ran
    REGISTRY = collections.OrderedDict()
    logger=None
        
    messageDict = {"Start": ["Function: {0}() called...",
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
    
    def __init__(self, *args, **kwargs):
        try:  
            self.set_credentials()
            self.notify=True # Always default to notify user

        except Exception as ex:
            # Consider adding traceback and error here
            NotifyMethods.log(status="ERROR", method=self.__class__.__name__, message="Connection to setting up notifications interupted, double check env variables", exception=ex)
            self.notify=False
        
        NotifyMethods.register(self)
        NotifyMethods.get_logger(kwargs)

    @classmethod
    def get_logger(cls, log=False, buffer=16384, **kwargs):
        """Sets up the class logger, should only need to be run once, although if you init it once 
        it'll always be active.

        Args:
            log (bool, optional): [whether to log the files]. Defaults to False.
            debug (bool, optional): [whether to enable debug mode]. Defaults to False.
            buffer (int, optional): [size of each log file]. Defaults to 10000.
        """        
        if os.getenv("LOG") or log: 
            if not os.path.isdir("logs"):
                os.mkdir("logs")

            path = os.getenv("LOGGER_PATH", os.getcwd())
            if path == "":
                path = os.getcwd() # If env variable but not defined is empty sets path to cwd

            import __main__ # Necessary for naming, setting up print formatting
            logger_name = __main__.__file__.split('/')[-1][:-3]
            logger_file_format = "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d"
            logger_console_format = "[%(levelname)s]: %(message)s"

            cls.logger = logging.getLogger(logger_name)
            cls.logger.setLevel(logging.ERROR)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.ERROR)
            console_handler.setFormatter(logging.Formatter(logger_console_format))
            cls.logger.addHandler(console_handler)

            file_handler = logging.handlers.RotatingFileHandler(filename="{}/logs/{}.log".format(path, logger_name), maxBytes=int(os.getenv("FILE_SIZE", default=buffer)), backupCount=2)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(logger_file_format))
            cls.logger.addHandler(file_handler)

            # Dictinoary houses all logging methdos
            cls.log_method_dict = {"DEBUG": cls.logger.debug,
                                    "INFO" : cls.logger.info,
                                    "ERROR": cls.logger.error,
                                    "WARNING": cls.logger.warning,}


    # Logger suite, functionos that control logging functinos that run
    @classmethod
    def set_logger(cls, level="DEBUG"):
        level_dict = {"DEBUG":logging.DEBUG,
                      "ERROR":logging.ERROR,
                      "INFO":logging.INFO,
                      "WARNING":logging.WARNING,}
        
        
        cls.logger.setLevel(level_dict.get(level, logging.DEBUG,))
        pass
    @classmethod
    def format_log(cls, method="", message="", exception="None", *args, **kwargs):
        return "[METHOD={}] Message = {}.\nException = {}.".format(method, message, exception)
    @classmethod
    def log(cls, status="DEBUG", *args, **kwargs):
        if cls.logger:
            log_message = cls.format_log(*args, **kwargs)
            cls.log_method_dict.get(status, lambda *args: [cls.logger.error("Logger method not found, using [ERROR]"), cls.logger.error(*args)])(log_message)

    @classmethod
    def register(cls, NotifyObject):
        """Registers each object and creates sa pseudo cyclical buffer that holds 3 objects that can be checked when youu grab the registry
        """ 
        if not NotifyObject.notify:
            NotifyObject = None
        cls.REGISTRY.setdefault(NotifyObject.__class__, collections.deque([], maxlen=3)).append(NotifyObject)
          
    @classmethod
    def get_registry(cls):
        return cls.REGISTRY

    @abstractmethod
    def set_credentials(self):
        pass

    # Suite of funcitons sends the messages for each different method. These guys help format each message for each of the instances
    @abstractmethod
    def send_start_MSG(self, func): 
        pass
    @abstractmethod
    def send_end_MSG(self, func, diff): 
        pass
    @abstractmethod
    def send_error_MSG(self): 
        pass

    @abstractmethod
    def send_message(self): 
        """Houses functions that interact with the respective platforms apis, the prior 3 all call this functioon to send the message
        """        
        pass
    
    def send_MSG_base(self, MSG):
        """All functions begin by calling send_MSG_base and depending on the status of that functioon, it'll be sent or
        an error will be logged if the initial credentials aren't valid

        Args:
            MSG ([str]): Current MSG to be sent. 
        """        
        try:
            if not self.notify:
                raise Exception("Error: Issue with initialized values, double check env variables/decorator arguments")

            self.send_message(MSG)
            NotifyMethods.log(status="DEBUG", method=self.__class__.__name__, message=MSG)

        except Exception as ex:
            NotifyMethods.log(status="ERROR", method=self.__class__.__name__, message=MSG, exception=ex)
              

    def format_message(cls, formatList, type_, msgDict=messageDict):
        return '\n'.join(msgDict[type_]).format(*formatList, machine=socket.gethostname())
