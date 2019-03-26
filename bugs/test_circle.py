import unittest
from circle import Circle

class TestCircle(unittest.TestCase): 
    
    def test_constructor(self):
        '''simply tests that a circle can be built'''
        c = Circle( center=(0,0), radius=2)
        with self.assertRaises(ValueError):
            Circle(radius=-1)
        
        
if __name__ == '__main__':
    unittest.main()
    