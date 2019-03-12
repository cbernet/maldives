import unittest
import os 
import glob
import h5py

class TestChain(unittest.TestCase):
    
    def test_chain(self):
        oldpwd = os.getcwd()
        os.chdir('test')
        files = glob.glob('xa*')
        for file in files: 
            os.remove(file)
        os.system('split -l 10 review100.json')
        os.chdir(oldpwd)
        os.system('python yelp_tokenize.py -p -d test "xa?"')
        os.system('python yelp_vocabulary.py -p -d test "xa?_tok.json"')
        os.system('python yelp_encode.py -p -d test "xa?_tok.json"')
        os.system('python yelp_fillarray.py -p -d test "xa?_enc.json"')
        h5 = h5py.File('test/data.h5')
        data = h5['reviews']    
        self.assertEqual(len(data),100)
        
        
if __name__ == '__main__':
    unittest.main()
