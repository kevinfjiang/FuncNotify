from . import *


class TestYagMail(TestAbstract):
    """Testing the text method of FuncNotify
    DisableTexts is set to True by default because I have limited
    money in my Twilio Accounts
    """  
    
    def test_Method(self, *args, **kwargs):
        time_func(self.wait_test, use_env=True, update_env=True, NotifyMethod="Email", *args, **kwargs)(**kwargs)
        self.confirm_method(EmailMethod)
        self.confirm_cred()
            
    def test_Decorator(self):
        time_Email(self.wait_test, update_env=True, use_env=True)()
        self.confirm_method(EmailMethod)
        self.confirm_cred()
    
    def test_Error(self):
        self.assertRaises(TException, time_Email(self.exception_test, use_env=True))
        self.confirm_method(EmailMethod)
        self.confirm_cred()
    
    def test_Stress(self): # Not stress testing to save the twilio money
        self.stress_method(self.test_Method, time_=5, count=5)
        for i in range(5):
            self.confirm_method(EmailMethod, n=i)
    