from . import *

class TestSlack(TestAbstract):
    """Testing the slack method of FuncNotify
    """    
    # Tests if slack alerts are working
    def test_Method(self, *args, **kwargs):
        time_func(self.wait_test, update_env=True, use_env=True, NotifyMethod="Slack", *args, **kwargs)(**kwargs)
        self.confirm_method(SlackMethod)
        self.confirm_cred()
        
    def test_Decorator(self):
        time_Slack(self.wait_test, update_env=True, use_env=True)()
        self.confirm_method(SlackMethod)
        self.confirm_cred()
        
    def test_Error(self):
        self.assertRaises(TException, time_Slack(self.exception_test, update_env=True, use_env=True))
        self.confirm_method(SlackMethod)
        self.confirm_cred()
    
    def test_Stress(self):
        self.stress_method(self.test_Method, time_=2, count=5)
        for i in range(5):
            self.confirm_method(SlackMethod, n=i)
            
    def test_bad_creds(self):
        time_Slack(self.wait_test, update_env=True, use_env=False, email=63)() # email should be a string noot int
        self.confirm_method(CredentialError)
        self.assertTrue(isinstance(self._get_last().NotifyObject, SlackMethod))
        self.assertTrue(isinstance(self._get_last().error, KeyError))
    
    # def test_bad_send(self):
    #  NOTE can't test this because can't easily change the credentials to bad ones during only send message
    #     time_Slack(self.wait_test, update_env=True, use_env=True, username="63")() # nonsensical email
    #     self.confirm_method(MessageSendError)
    #     self.assertTrue(isinstance(self._get_last().NotifyObject, SlackMethod))
    #     self.assertTrue(isinstance(self._get_last().error, Exception))
        