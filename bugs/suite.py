import unittest

from test_circle import TestCircle
from test_skip import TestSkip1, TestSkip2
from test_alwaysok import TestAlwaysOk

testcases = [
    TestAlwaysOk,
    TestCircle,
    TestSkip1,
    TestSkip2    
]

suite = unittest.TestSuite()

loader = unittest.TestLoader()
for test_class in testcases:
    tests = loader.loadTestsFromTestCase(test_class)
    suite.addTests(tests)

if __name__ == '__main__':  
    import sys
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
