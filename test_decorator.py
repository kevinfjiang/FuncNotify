import NotifyDecorators
from Methods import *

import unittest
import time
import os

wastemoney = False

class TestDecorator(unittest.TestCase):
    """Note will not actually test decorator but an equivalent variation
    """ 
    # Basic notify method, testing it works   
    def test_PrintDef(self, *args, **kwargs):
        NotifyDecorators.time_func(wait_test, True, *args, **kwargs)(**kwargs)
        self.confirm_method(PrintMethod)
        self.confirm_cred()

    # Base tests, testing NotifyMethod features
    def test_ENV(self, *args, **kwargs):
        NotifyDecorators.time_func(wait_test, True, *args, **kwargs)(**kwargs)
        self.confirm_dotenv("ALIVE")
    def test_DeadENV(self, *args, **kwargs):
        NotifyDecorators.time_func(wait_test, False, *args, **kwargs)(**kwargs)
        self.confirm_dotenv(None)

    # Tests for slack notify methds
    def test_slack(self, *args, **kwargs):
        pass
    def test_slackfunc(self, *args, **kwargs):
        pass
    
    # Tests if text alerts are working, set waste money to true if u want to test, costs money
    def test_text(self, *args, **kwargs):
        if wastemoney:
            NotifyDecorators.time_func(wait_test, True, "Text", *args, **kwargs)()
            self.confirm_method(TextMethod)
            self.confirm_cred()
    def test_textfunc(self, *args, **kwargs):
        if wastemoney:
            NotifyDecorators.time_text(wait_test, True, *args, **kwargs)()
            self.confirm_method(TextMethod)
            self.confirm_cred()

    # Stress testing
    def test_stressPrint(self):
        self.stressMethod(self.test_PrintDef, time_=.01, verbose=False)
    def test_stressSlack(self):
        self.stressMethod(self.test_slack, time_=1, count=60)


    def stressMethod(self, method, count=100, *args, **kwargs):
        for _ in range(count):
            method(*args, **kwargs)

    def confirm_dotenv(self, env_val):
        self.assertEqual(os.getenv('TEST_ENV'), env_val)
    def confirm_method(self, methodName):
        self.assertEqual(list(NotifyMethods.get_registry().keys())[-1], methodName)
    def confirm_cred(self):
        self.assertTrue(list(NotifyMethods.get_registry().values())[-1][-1].notify)


def wait_test(time_=.25, **kwargs):
    time.sleep(time_)

if __name__ == '__main__':
    unittest.main()