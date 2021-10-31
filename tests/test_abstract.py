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
    """Will not test this Class because of ABCAstractEnableTests disables this test,
    which is intended because this is an abstract class
    """ 
    @abstractmethod
    def test_Method(self, *args, **kwargs):
        pass
    @abstractmethod
    def test_Decorator(self):
        pass
    @abstractmethod
    def test_Error(self):
        pass
    @abstractmethod
    def test_Stress(self):
        pass
    
    
    
    # Basic notify method, testing it works   
    def stress_method(self, func, count=100, *args, **kwargs):
        for _ in range(count):
            func(*args, **kwargs)

    def _get_last(self, n: int=-1): # Returns last nth character, 
                                    # be careful not to go too big
        return NotifyMethods.get_buffer()[n]
    
    def confirm_method(self, methodName, n: int=-1):
        self.assertEqual(type(self._get_last(n)), methodName)
    def confirm_cred(self, n: int=-1):
        self.assertEqual(self._get_last(n)._error, None)
    
    def wait_test(self, time_=.25, *args, **kwargs):
        time.sleep(time_)
    def exception_test(self, *args, **kwargs):
        raise TException

class TException(Exception):
    """Only here to ensure that when we test raisisng exception, 
    tests always get this specific exception
    stands for TestException.
    """    
    pass


if __name__ == '__main__':
    unittest.main()