from . import *

class PrintTest(TestGeneric):
    """Tests generic printmethood with ENV tests
    __test__ needs to be set to True in order to be tested,
    The parent TestGeneric is abstract so it is previously set as false
    """     
    def test_Method(self, *args, **kwargs):
        time_func(self.wait_test, use_env=True, *args, **kwargs)(**kwargs)
        self.confirm_method(PrintMethod)
        self.confirm_cred()

    def test_Decorator(self, *args, **kwargs):
        time_func(self.wait_test, use_env=True, *args, **kwargs)(**kwargs)
        self.confirm_method(PrintMethod)
        self.confirm_cred()
    
    # Base tests, testing NotifyMethod features
    def test_ENV(self, *args, **kwargs):
        time_func(self.wait_test, update_env=True, use_env=True, *args, **kwargs)(**kwargs)
        self.confirm_dotenv("ALIVE")
    def test_DeadENV(self, *args, **kwargs):
        time_func(self.wait_test, update_env=True, use_env=False, *args, **kwargs)(**kwargs)
        self.confirm_dotenv(None)

    #  Stress testing
    def test_Stress(self):
        self.stressMethod(self.test_Method, time_=.01, verbose=False)
        # Tests for slack notify methds