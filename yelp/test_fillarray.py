import unittest
from yelp_fillarray import process_file, finalize
import h5py

import os 

class TestFillarray(unittest.TestCase):
    
    def setUp(self):
        self.oldpwd = os.getcwd()
        os.chdir('test')
        
    def tearDown(self):
        os.chdir(self.oldpwd)
        
    def test_1(self):
        import test.options as options
        options.keep_unknown = False
        options.nwords = 250
        fname = 'review100_enc.json'
        results = [process_file(fname, options)]
        finalize(results)
        # output file exists
        self.assertTrue(os.path.isfile('data.h5'))
        # same number of lines as in input file
        h5 = h5py.File('data.h5')
        data = h5['reviews']
        with open(fname) as ifile: 
            self.assertEqual(len(ifile.readlines()), 
                             len(data))
        