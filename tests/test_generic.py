from FuncNotify import *

import unittest
import time
import os

class TestGeneric(unittest.TestCase):
    """Note will not actually test decorator but an equivalent variation
    """ 
    # Basic notify method, testing it works   
    def test_PrintDef(self, *args, **kwargs):
        time_func(self.wait_test, True, *args, **kwargs)(**kwargs)
        self.confirm_method(PrintMethod)
        self.confirm_cred()

    # Base tests, testing NotifyMethod features
    def test_ENV(self, *args, **kwargs):
        time_func(self.wait_test, True, *args, **kwargs)(**kwargs)
        self.confirm_dotenv("ALIVE")
    def test_DeadENV(self, *args, **kwargs):
        time_func(self.wait_test, False, *args, **kwargs)(**kwargs)
        self.confirm_dotenv(None)

    #  Stress testing
    def test_stressPrint(self):
        self.stressMethod(self.test_PrintDef, time_=.01, verbose=False)
        # Tests for slack notify methds

    def stressMethod(self, method, count=100, *args, **kwargs):
        for _ in range(count):
            method(*args, **kwargs)

    def confirm_dotenv(self, env_val):
        self.assertEqual(os.getenv('TEST_ENV'), env_val)
    def confirm_method(self, methodName):
        self.assertEqual(type(NotifyMethods.get_registry()[-1]), methodName)
    def confirm_cred(self):
        self.assertTrue(NotifyMethods.get_registry()[-1].notify)
    
    def wait_test(self, time_=.25, **kwargs):
        time.sleep(time_)

if __name__ == '__main__':
    unittest.main()