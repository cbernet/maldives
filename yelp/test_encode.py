import unittest
from yelp_encode import process_file, output_fname
from vocabulary import Vocabulary

import os 
import json


class TestEncode(unittest.TestCase):
    
    def setUp(self):
        self.oldpwd = os.getcwd()
        os.chdir('test')
        
    def tearDown(self):
        os.chdir(self.oldpwd)
        
    def test_1(self):
        import test.options as options
        fname = 'review100_tok.json'
        voc = Vocabulary.load('vocabulary')
        process_file(fname, options, voc)
        # output file name exists
        outfname = output_fname(fname)
        self.assertTrue(os.path.isfile(outfname))
        with open(outfname) as outf:
            outlines = outf.readlines()
            data = json.loads(outlines[0])
            # encoding worked
            self.assertListEqual(
                data['text'],
                [754, 570, 1, 5, 755, 38, 55, 72, 54, 1142, 1, 222, 1143, 189, 12, 1, 1144, 1, 432, 60, 54, 1145, 1, 223, 756, 1, 1, 433, 757, 1, 756, 57, 1, 12, 1, 1146, 1147, 190, 2, 351, 1148, 1149, 11, 24, 1150, 1]
            )
            with open(fname) as inf:
                inlines = inf.readlines()
                # same number of lines as in the input file   
                self.assertEqual(len(outlines), len(inlines))
                
        