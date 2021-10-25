from . import *


class TestText(TestAbstract):
    """Testing the text method of FuncNotify
    DisableTexts is set to True by default because I have limited
    money in my Twilio Accounts
    """  
    __test__=False # Not testing because Twilio gives me a limited budget
                   # Which I've almost entirely used up, lol
    
    def test_Method(self, *args, **kwargs):
        time_func(self.wait_test, use_env=True, update_env=True, NotifyMethod="Text", *args, **kwargs)(**kwargs)
        self.confirm_method(TextMethod)
        self.confirm_cred()
            
    def test_Decorator(self):
        time_Text(self.wait_test, update_env=True, use_env=True)()
        self.confirm_method(TextMethod)
        self.confirm_cred()
    
    def test_Error(self):
        self.assertRaises(TException, time_Text(self.exception_test, use_env=True))
        self.confirm_method(TextMethod)
        self.confirm_cred()
    
    def test_Stress(self):
        self.stress_method(self.test_Method, time_=2, count=5)
    