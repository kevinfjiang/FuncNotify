from . import *

class PrintTest(TestAbstract):
    """Tests generic printmethood with ENV tests
    __test__ needs to be set to True in order to be tested,
    The parent TestGeneric is abstract so it is previously set as false
    """     
    def test_Method(self, *args, **kwargs):
        time_func(self.wait_test, NotifyMethod="Print", use_env=True, *args, **kwargs)(**kwargs)
        self.confirm_method(PrintMethod)
        self.confirm_cred()

    def test_Decorator(self):
        time_func(self.wait_test, NotifyMethod="Print", use_env=True)()
        self.confirm_method(PrintMethod)
        self.confirm_cred()
        
    def test_Error(self):
        self.assertRaises(TException, time_func(self.exception_test, NotifyMethod="Print", use_env=True))
        self.confirm_method(PrintMethod)
        self.confirm_cred()
    #  Stress testing
    def test_Stress(self):
        self.stress_method(self.test_Method, time_=.01, verbose=False)
        # Tests for slack notify methds
        
    #Env testing
    def test_ENV(self):
        time_func(self.wait_test, NotifyMethod="Print", update_env=True, use_env=True)()
        self.assertTrue(self._get_last(-1).environ_dict)
    def test_DeadENV(self):
        time_func(self.wait_test, NotifyMethod="Print", update_env=True, use_env=False)()
        self.assertFalse(self._get_last(-1).environ_dict)
        
    #Multi target message sending
    def test_multi_target(self):
        kwargs1 = {'NotifyMethod': "Print", 'use_env': True, 'verbose': True}
        kwargs2 = {'NotifyMethod': "Print", 'use_env': True, 'verbose': False}
        time_func(self.wait_test, multi_target=[kwargs1, kwargs2])()
        self.assertFalse(self._get_last(-1).verbose)
        self.assertTrue(self._get_last(-2).verbose)
        self.confirm_method(PrintMethod)
        
    def test_multi_env(self):
        time_func(self.wait_test, NotifyMethod="Print", use_env=False, multi_env=[".env", ""])()
        self.assertTrue(self._get_last(-2).environ_dict)
        self.assertFalse(self._get_last(-1).environ_dict)
        self.confirm_method(PrintMethod)
        
    def test_multi_env_target(self):
        kwargs1 = {'NotifyMethod': "Print", 'use_env': True, 'verbose': True}
        kwargs2 = {'NotifyMethod': "Print", 'use_env': True, 'verbose': False}
        time_func(self.wait_test, 
                                     multi_target=[kwargs1, kwargs2, kwargs2, kwargs1], 
                                     multi_env=[".env", "", ".env", ""])()
        self.assertTrue(self._get_last(-1).verbose)
        self.assertFalse(self._get_last(-1).environ_dict)
        self.assertFalse(self._get_last(-2).verbose)
        self.assertTrue(self._get_last(-2).environ_dict)
        self.assertFalse(self._get_last(-3).verbose)
        self.assertFalse(self._get_last(-3).environ_dict)
        self.assertTrue(self._get_last(-4).verbose)
        self.assertTrue(self._get_last(-4).environ_dict)
        
        for i in range(-1, -5, -1):
            self.confirm_method(PrintMethod, n=i)
            
    # Bad args
    def test_bad_method(self):
        with self.assertWarnsRegex(UserWarning, "a;lksdkfa;dfkwa"), self.assertLogs(NotifyMethods.logger, logging.DEBUG):
            NotifyMethods.set_logger(logging.DEBUG)
            time_func(self.wait_test, NotifyMethod="a;lksdkfa;dfkwa", update_env=True, use_env=True)()
            
        self.confirm_method(PrintMethod)
        self.confirm_cred()
        
    def test_logger(self):
        import __main__
        self.assertEqual(NotifyMethods.logger.name, __main__.__file__.split('/')[-1].split('.')[0])
        with self.assertLogs(NotifyMethods.logger, logging.ERROR):
            NotifyMethods.set_logger(logging.DEBUG) # Verbose needs to be bool, not string
            time_func(self.wait_test, NotifyMethod="Print", verbose="ad;fkafd", use_log=True, use_env=False) 
        with self.assertNoLogs(NotifyMethods.logger, logging.ERROR):
            NotifyMethods.set_logger(logging.CRITICAL) 
            time_func(self.wait_test, NotifyMethod="Print", verbose="ad;fkafd", use_env=False)
    
    def test_mute(self):
        with self.assertNoLogs(NotifyMethods.logger, logging.INFO):
            NotifyMethods.set_mute(True) 
            time_func(self.wait_test, NotifyMethod="Print", verbose=True)()
        
        with self.assertLogs(NotifyMethods.logger, logging.DEBUG):
            NotifyMethods.set_mute(False) 
            time_func(self.wait_test, NotifyMethod="Print", verbose=True)()