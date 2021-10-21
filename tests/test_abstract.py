from abc import ABCMeta, abstractmethod
import inspect
import unittest
import time

from FuncNotify import *

class ABCAstractEnableTests(ABCMeta):
    def __new__(cls, clsname, bases, attrs):
        """You must disable __test__ for TestGeneric because it's abstract, 
        this is the way I've choosen to do it with minimal headache for test writers.
        """        
        newclass = super(ABCAstractEnableTests, cls).__new__(cls, clsname, bases, attrs)
        newclass.__test__ = (not inspect.isabstract(newclass)) and newclass.__dict__.get("__test__", True)
        # Necessary for allowing __test__ to still disable tests, and preventing abstract
        # tests classes from being instantiated, without this, it would instatiate `TestAbstract` and error
        
        return newclass
    

class TestAbstract(unittest.TestCase, metaclass=ABCAstractEnableTests):
    """Will not test this Class because of ABCAstractEnableTests disabless this test,
    which is intended because this is an abstract class
    """ 
    @abstractmethod
    def test_Method(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def test_Decorator(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def test_Stress(self):
        pass
    
    
    # Basic notify method, testing it works   
    def stress_method(self, method, count=100, *args, **kwargs):
        for _ in range(count):
            method(*args, **kwargs)

    def _get_last(self):
        return NotifyMethods.get_registry()[-1]
    
    def confirm_dotenv(self, env_val):
        self.assertEqual(self._get_last().environ_dict.get('TEST_ENV'), env_val)
    def confirm_method(self, methodName):
        self.assertEqual(type(self._get_last()), methodName)
    def confirm_cred(self):
        self.assertEqual(self._get_last().error, None)
    
    def wait_test(self, time_=.25, *args, **kwargs):
        time.sleep(time_)



if __name__ == '__main__':
    unittest.main()