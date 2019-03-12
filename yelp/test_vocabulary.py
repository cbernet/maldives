from vocabulary import Vocabulary
from yelp_vocabulary import process_file

import unittest
from collections import Counter
import pickle
import os

class TestVocabulary(unittest.TestCase):
    
    def test_class(self):
        sentence = ['the','little', 'red', 'hood', 
                    'and', 'the', 'wolf', 'are', 'both', 'red']
        counter = Counter(sentence)
        voc = Vocabulary(counter)
        # test a simple case, and check frequency ordering
        self.assertListEqual(voc.words, 
                             ['<PAD>', '<UNK>', 'the', 'red', 'little', 
                              'hood', 'and', 'wolf', 
                              'are', 'both'])
        # test index consistency
        for i, word in enumerate(voc.words):
            self.assertEqual(i, voc.index[word])
        
        # test write 
        voc.save('voc')
        # test reading, bare pck
        with open('voc.pck','rb') as pckfile:
            voc2 = pickle.load(pckfile)
        # test reading, class method
        voc3 = Vocabulary.load('voc')
        self.assertListEqual(voc3.words,
                             voc.words)
        self.assertDictEqual(voc3.index,
                             voc.index)
        os.remove('voc.pck')
        
    def test_script(self):
        import test.options as options
        options.nwords = 20000
        fname = 'test/review100_tok.json'
        # test that the script runs 
        counter = process_file(fname, options)
        voc = Vocabulary(counter, n_most_common=options.nwords)
        # and that it produces the same results as the reference
        voc_ref = Vocabulary.load('test/vocabulary')
        self.assertListEqual(voc.words, voc_ref.words)
        self.assertDictEqual(voc.index, voc_ref.index)
        