from . import *


class TestText(TestAbstract):
    """Testing the text method of FuncNotify
    DisableTexts is set to True by default because I have limited
    money in my Twilio Accounts
    """  
    DisableTexts=True 
    def test_Method(self, *args, **kwargs):
        if TestText.DisableTexts:
            return
        time_func(self.wait_test, use_env=True, update_env=True, NotifyMethod="Text", *args, **kwargs)(**kwargs)
        self.confirm_method(TextMethod)
        self.confirm_cred()
            
    def test_Decorator(self, *args, **kwargs):
        if TestText.DisableTexts:
            return
        time_Text(wait_test, use_env=True, *args, **kwargs)()
        self.confirm_method(TextMethod)
        self.confirm_cred()
    
    def test_Stress(self):
        if TestText.DisableTexts:
            return
        self.stressMethod(self.test_Method, time_=2, count=5)
    