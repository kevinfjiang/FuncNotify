"""In order to contribute to TestGeneric, one can either write a new file for a
new Method to ensure coverage (see `test_slack` for an example). Additionally, you
can write more coverage for `test_generic` for other test_classes to inheirit. Make sure
any new NotifyMethods notify Kevin.
"""
from tests.test_abstract import *
from FuncNotify import *
import pytest
import sys
version_skip = pytest.mark.skipif(sys.version_info < (3, 10), reason="Nologs requires python3.10 or higher") 