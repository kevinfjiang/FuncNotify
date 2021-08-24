import time
from NotifyMethods import *

# dm feature, shouldn't be that hard, especially with some local info
DefaultNotify=None

# Include some features to include more features, ie time, machinen, etc look here https://github.com/huggingface/knockknock
#TODO for the individual functionns, add the optionn to include keyword argumetns, as well as into the kwargs args
NotifyType = {"Default": PrintMethod, 
            "Slack": SlackMethod, # TODO add more
            "Text": TextMethod,
}

def timerBase(func, NotifyObj, *args, **kwargs):# TODO Rewrite to give more information, format this better too, like include a string of information
    # Consider creating a template of this, where you can enact functions based on the ttemplates that it appears like, like
    # Each of objects have a method send_message, could be very clever!!!! work on this for an hr tn!!!!!!
    try:
        NotifyObj.sendStartMSG(func)
        start=time.time()

        result = func(*args, **kwargs)
        
        end=time.time()
        NotifyObj.sendEndMSG(func, end-start)
    
    except Exception as ex:
        NotifyObj.sendErrorMSG(func, ex)
        raise ex
    return result

# Main wrapper
def time_func(Alert=DefaultNotify, funcSpecify="Default", *args2, **kwargs2): # Include support for slack and also include error checking/handeling
    if funcSpecify not in NotifyType:
        raise Exception #TODO include custom exception
    
    def timeFunction(func):
        def timer(*args, **kwargs):
            result = timerBase(func, NotifyType[funcSpecify](*args2, **kwargs2), *args, **kwargs)
            return result
        return timer

    if callable(Alert):
        func = Alert
        Alert = DefaultNotify
        return timeFunction(func)
    return timeFunction

def time_text(Alert=DefaultNotify, *args, **kwargs): # Include something to check the rest of the arguments in the word
    return time_func(Alert, "Text") 
    
def time_slack(Alert=DefaultNotify, *args, **kwargs):
    return time_func(Alert, "Slack") 

