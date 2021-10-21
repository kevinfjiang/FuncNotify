from . import *

class TestTeams(TestAbstract):
    """Testing the Teams method of FuncNotify
    """   
    __test__ = False # Allows dissabling of tests
    
    # Tests if Teams alerts are working
    def test_Method(self, *args, **kwargs):
        time_func(self.wait_test, update_env=True, use_env=True, NotifyMethod="Teams", *args, **kwargs)(**kwargs)
        self.confirm_method(TeamsMethod)
        self.confirm_cred()
        
    def test_Decorator(self, *args, **kwargs):
        time_Teams(self.wait_test, use_env=True, *args, **kwargs)()
        self.confirm_method(TeamsMethod)
        self.confirm_cred()
        
    def test_Stress(self):
        self.stress_method(self.test_Method, time_=5, count=5)