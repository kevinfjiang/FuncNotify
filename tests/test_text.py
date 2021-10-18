from . import *


class TestText(TestGeneric):
    """Testing the text method of FuncNotify
    """  
    wastemoney=False  
    # Tests if text alerts are working, set waste money to true if u want to test, costs money
    def test_text(self, *args, **kwargs):
        if TestText.wastemoney:
            time_func(self.wait_test, use_env=True, update_env=True, NotifyMethod="Text", *args, **kwargs)()
            self.confirm_method(TextMethod)
            self.confirm_cred()
    def test_textfunc(self, *args, **kwargs):
        if TestText.wastemoney:
            time_Text(wait_test, use_env=True, *args, **kwargs)()
            self.confirm_method(TextMethod)
            self.confirm_cred()