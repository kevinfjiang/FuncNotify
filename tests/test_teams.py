from FuncNotify.TeamsMethod import TeamsMethod
from . import *

class TestTeams(TestGeneric):
    """Testing the Teams method of FuncNotify
    """    
    
    # Tests if Teams alerts are working
    def test_teams(self, *args, **kwargs):
        time_func(self.wait_test, update_env=True, use_env=True, NotifyMethod="Teams", *args, **kwargs)(**kwargs)
        self.confirm_method(TeamsMethod)
        self.confirm_cred()
        
    def test_teamsfunc(self, *args, **kwargs):
        time_Teams(self.wait_test, use_env=True, *args, **kwargs)()
        self.confirm_method(TeamsMethod)
        self.confirm_cred()
        
    def test_stressSlack(self):
        self.stressMethod(self.test_slack, time_=5, count=10)