import os
import socket
import time

from abc import ABC, abstractmethod
from twilio.rest import Client

from slack import WebClient
from slack.errors import SlackApiError


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class NotifyMethods(ABC):

    messageDict = {"Start": ["Function: {0}() called...",
                            "Machine Name: {machine}",
                            "Start Time: {1}"],
                   "End":   ["Function: {0}() completed",
                            "Machine Name: {machine}",
                            "Finish Time: {1}",
                            "Total Time: {2:.2f}"],
                   "Error": ["Place"]} #TODO include error messages
    
    def __init__(self):
        self.notify=True
        self.client=None # Not necessary but I wanted to define it anyways

    def sendStartMSG(self, func): # Used for formatting and sending
        MSG = self.formatMessage(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime())], type_="Start")
        if self.notify:
            self.send_message(MSG)
        else:
            self.sendDefMSG(MSG)

    def sendEndMSG(self, func, diff): # Used for formatting and sending
        MSG = self.formatMessage(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime()), diff], type_="End")
        if self.notify:
            self.send_message(MSG)
        else:
            self.sendDefMSG(MSG)
    
    def sendErrorMSG(self): # Used for sending error messagges
        pass

    @abstractmethod
    def send_message(self): # Used for the actual API interaction
        pass
    
    def sendDefMSG(self, MSG):
        print("Error: Error occurred when delivering message of type {}".format(type(self)))
        print(MSG)

    def formatMessage(self, formatList:list, type_:str, msgDict=messageDict):
        return '\n'.join(msgDict[type_]).format(*formatList, machine=socket.gethostname())


class TextMethod(NotifyMethods):
    def __init__(self):
        super().__init__()
        try:
            self.cellphone = os.getenv("PHONE")
            self.twilio_number = os.getenv("TWILIOPHONE")
            self.client = Client(os.getenv("TWILIOACCOUNT"), os.getenv("TWILIOTOKEN"))

        except Exception:
            print("ERROR: your environment credentials aren't valid, this won't terminate the function \
                   but you will not be properly notified on completion")
            self.notify=False

    def send_message(self, message):
        try:
            self.client.messages.create(to=self.cellphone,
                            from_=self.twilio_number,
                            body=message)
        except Exception as e:
            print("Exception: Occurred while delivering message" + str(e))
            super().sendDefMSG(message)
        

class SlackMethod(NotifyMethods):
    def __init__(self):
        super().__init__()
        try:
            slackToken = os.getenv("SLACK_API_TOKEN")
            self.client = WebClient(token=slackToken)
            self.email = os.getenv("EMAIL")
        except Exception:
            self.notify=False

    def send_message(self, message):
        try:
            response = self.client.chat_postMessage(username="alerty", 
                                                text=message,
                                                channel=self.client.users_lookupByEmail(email=self.email)['user']['id'])

        except Exception as e:
            print("Exception: Occurred while delivering message " + str(e))
            super().sendDefMSG(message)

class PrintMethod(NotifyMethods):

    def send_message(self):
        pass
    pass

def formatError(e: Exception)->str:
    #return "Error found: \nType:{} \nMessage:{}\nTraceback:{}".format(type(e), e, traceback.format_exc())
    pass