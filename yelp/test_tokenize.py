import unittest
from yelp_tokenize import process_file, output_fname

import os 
import json

fname = 'review_100.json'

class TestTokenize(unittest.TestCase):
    
    def setUp(self):
        self.oldpwd = os.getcwd()
        os.chdir('test')
        
    def tearDown(self):
        os.chdir(self.oldpwd)
        
    def test_1(self):
        import test.options as options
        process_file(fname, options)
        # output file name exists
        outfname = output_fname(fname)
        self.assertTrue(os.path.isfile(outfname))
        with open(outfname) as outf:
            outlines = outf.readlines()
            data = json.loads(outlines[0])
            # tokenization worked
            self.assertListEqual(data['text'], 
                                 ["total", "bill", "for", "this", "horrible", "service", "?", "over", "$", "8gs", ".", "these", "crooks", "actually", "had", "the", "nerve", "to", "charge", "us", "$", "69", "for", "3", "pills", ".", "i", "checked", "online", "the", "pills", "can", "be", "had", "for", "19", "cents", "each", "!", "avoid", "hospital", "ers", "at", "all", "costs", "."])
            with open(fname) as inf:
                inlines = inf.readlines()
                # same number of lines as in the input file   
                self.assertEqual(len(outlines), len(inlines))
                
        