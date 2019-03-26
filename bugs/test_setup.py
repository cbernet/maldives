import unittest
import os 

class TestSetup(unittest.TestCase): 
    
    def setUp(self): 
        self.testfname = 'testfile.txt'
        if not os.path.isfile(self.testfname):
            with open(self.testfname, 'w') as ifile: 
                print('creating test file')
                testlines = ['first line\n', 'second line\n']
                ifile.writelines(testlines)
                
    def test_nlines(self):
        with open(self.testfname) as ifile:
            self.assertEqual(len(ifile.readlines()),2)
            
    def test_lines(self): 
        with open(self.testfname) as ifile:
            self.assertListEqual(ifile.readlines(),
                                 ['first line\n', 'second line\n'])
               
if __name__  == '__main__':
    unittest.main()