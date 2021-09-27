from . import *
from FuncNotify import *

class PrintTest(TestGeneric):
    """Tests generic printmethood with ENV tests
    """    
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