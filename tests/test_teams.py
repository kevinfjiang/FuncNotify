from . import *

class TestSlack(TestGeneric):
    """Testing the slack method of FuncNotify
    """    
    
    # Tests if slack alerts are working
    def test_slack(self, *args, **kwargs):
        time_func(self.wait_test, update_env=True, use_env=True, NotifyMethod="Slack", *args, **kwargs)(**kwargs)
        self.confirm_method(SlackMethod)
        self.confirm_cred()
        
    def test_slackfunc(self, *args, **kwargs):
        time_Slack(self.wait_test, use_env=True, *args, **kwargs)()
        self.confirm_method(SlackMethod)
        self.confirm_cred()
        
    def test_stressSlack(self):
        self.stressMethod(self.test_slack, time_=5, count=10)