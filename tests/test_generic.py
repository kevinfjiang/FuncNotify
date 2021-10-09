from FuncNotify import *

import unittest
import time
import os

class TestGeneric(unittest.TestCase):
    """Note will not actually test decorator but an equivalent variation
    """ 
    # Basic notify method, testing it works   
    def stressMethod(self, method, count=100, *args, **kwargs):
        for _ in range(count):
            method(*args, **kwargs)

    def _get_last(self):
        return NotifyMethods.get_registry()[-1]
    
    def confirm_dotenv(self, env_val):
        self.assertEqual(self._get_last().environ_dict.get('TEST_ENV'), env_val)
    def confirm_method(self, methodName):
        self.assertEqual(type(self._get_last()), methodName)
    def confirm_cred(self):
        self.assertEqual(self._get_last().error, None)
    
    def wait_test(self, time_=.25, *args, **kwargs):
        time.sleep(time_)

if __name__ == '__main__':
    unittest.main()