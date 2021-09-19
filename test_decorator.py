from Methods import *
import unittest
import time
import os
import NotifyDecorators

wastemoney = False

class TestDecorator(unittest.TestCase):
    """Note will not actually test decorator but an equivalent variation
    """    
    def test_PrintDef(self):
        NotifyDecorators.time_func(waitOne, True)()
        self.confirm_method(PrintMethod)
        self.confirm_cred()

    def test_text(self):
        if wastemoney:
            NotifyDecorators.time_func(waitOne, True, "Text")()
            self.confirm_method(TextMethod)
            self.confirm_cred()
    
    def test_textfunc(self):
        if wastemoney:
            NotifyDecorators.time_text(waitOne, True)()
            self.confirm_method(TextMethod)
            self.confirm_cred()

    def test_ENV(self):
        NotifyDecorators.time_func(waitOne, True)()
        self.confirm_dotenv("ALIVE")

    def test_DeadENV(self):
        NotifyDecorators.time_func(waitOne, False)()
        self.confirm_dotenv(None)

    def test_Stress(self):
        for _ in range(100):
            NotifyDecorators.time_func(waitOne, dot_env=True, verbose=False)(.001)

    def confirm_dotenv(self, env_val):
        self.assertEqual(os.getenv('TEST_ENV'), env_val)

    def confirm_method(self, methodName):
        self.assertEqual(list(NotifyMethods.get_registry().keys())[-1], methodName)
    
    def confirm_cred(self):
        self.assertTrue(list(NotifyMethods.get_registry().values())[-1][-1].notify)




def waitOne(tim=.25):
    time.sleep(tim)

if __name__ == '__main__':
    unittest.main()