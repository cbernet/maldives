import unittest
import datetime
import getpass

now = datetime.datetime.now().time()
noon = datetime.time(12,0)
evening = datetime.time(19,0)

user = getpass.getuser()

class TestSkip1(unittest.TestCase): 
    
    @unittest.skipIf(now<noon or now>evening, 
                     'only testing in the afternoon')
    def test_1(self): 
        '''tested in the afternoon only'''
        self.assertTrue(True)
        

@unittest.skipIf(user!='cbernet',"these are colin's private tests")
class TestSkip2(unittest.TestCase):
    
    def test_1(self):
        self.assertTrue(True)

    def test_2(self):
        self.assertTrue(True)

        
if __name__=='__main__':
    unittest.main()