import os
import sys
import socket
import time
import traceback

from abc import ABCMeta, abstractmethod
from twilio.rest import Client

if sys.version_info < (3,0): 
    from slackclient import SlackClient
else:
    from slack import WebClient


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

class NotifyMethods():
    __metaclass__ = ABCMeta   
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
    
    def __init__(self):
        self.notify=True
        self.client=None # Not necessary but I wanted to define it anyways
        
    @abstractmethod
    def sendStartMSG(self, func): # Used for formatting and sending
        pass
    
    @abstractmethod
    def sendEndMSG(self, func, diff): # Used for formatting and sending
        pass
    
    @abstractmethod
    def sendErrorMSG(self): # Used for sending error messagges
        pass

    @abstractmethod
    def send_message(self): # Used for the actual API interaction
        pass
    
    def sendDefMSG(self, MSG):
        print("Error: Error occurred when delivering message of method {}".format(type(self)))
        print(MSG)

    def formatMessage(self, formatList, type_, msgDict=messageDict):
        return '\n'.join(msgDict[type_]).format(*formatList, machine=socket.gethostname())


class TextMethod(NotifyMethods):
    def __init__(self, cellphone=None):
        super(TextMethod, self).__init__()
        try:
            self.cellphone = os.getenv("PHONE")
            self.twilio_number = os.getenv("TWILIOPHONE")
            self.client = Client(os.getenv("TWILIOACCOUNT"), os.getenv("TWILIOTOKEN"))

        except Exception:
            print("ERROR: your environment credentials aren't valid, this won't terminate the function \
                   but you will not be properly notified on completion")
            self.notify=False

    def sendStartMSG(self, MSG):
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

    def sendErrorMSG(self, func, e):
        MSG = self.formatMessage(formatList=[func.__name__, type(e), str(e), time.strftime(DATE_FORMAT, time.localtime()),traceback.format_exc()], type_="Error")+":taraduckface:"
        if self.notify:
            self.send_message(MSG)
        else:
            self.sendDefMSG(MSG)

    def send_message(self, message):
        try:
            self.client.messages.create(to=self.cellphone,
                            from_=self.twilio_number,
                            body=message)
        except Exception as e:
            super(TextMethod, self).sendDefMSG(message)
        

class SlackMethod(NotifyMethods):
    def __init__(self, email=None):
        super(SlackMethod, self).__init__()
        try:
            slackToken = os.getenv("SLACK_API_TOKEN")
            if sys.version_info < (3,0):
                self.client = SlackClient(slackToken)
            else:
                self.client = WebClient(token=slackToken)
            
            if email is None:
                self.email = os.getenv("EMAIL")
            else:
                self.email=email

        except Exception:
            self.notify=False

    def sendStartMSG(self, func):
        MSG = self.formatMessage(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime())], type_="Start")+":party_blob:"
        if self.notify:
            self.send_message(MSG)
        else:
            self.sendDefMSG(MSG)

    def sendEndMSG(self, func, diff): # Used for formatting and sending
        MSG = self.formatMessage(formatList=[func.__name__, time.strftime(DATE_FORMAT, time.localtime()), diff], type_="End")+":tada:"
        if self.notify:
            self.send_message(MSG)
        else:
            self.sendDefMSG(MSG)

    def sendErrorMSG(self, func, e):
        MSG = self.formatMessage(formatList=[func.__name__, type(e), str(e), time.strftime(DATE_FORMAT, time.localtime()),traceback.format_exc()], type_="Error")+":taraduckface:"
        if self.notify:
            self.send_message(MSG)
        else:
            self.sendDefMSG(MSG)

    def send_message(self, message):
        try:
            if sys.version_info < (3,0):
                self.client.api_call("chat.postMessage",
                                    username="alerty",
                                    channel=self.client.api_call(
                                                                "users.lookupByEmail",
                                                                email=self.email)['user']['id'],
                                    text=message)     
            else:
                response = self.client.chat_postMessage(username="alerty", 
                                                    text=message,
                                                    channel=self.client.users_lookupByEmail(email=self.email)['user']['id'])

        except Exception as e:
            super(SlackMethod, self).sendDefMSG(message)

class PrintMethod(NotifyMethods):

    def sendStartMSG(self, MSG):
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

    def sendErrorMSG(self, func, e):
        MSG = self.formatMessage(formatList=[func.__name__, type(e), str(e), time.strftime(DATE_FORMAT, time.localtime()),traceback.format_exc()], type_="Error")+":taraduckface:"
        if self.notify:
            self.send_message(MSG)
        else:
            self.sendDefMSG(MSG)

    def send_message(self):
        pass
