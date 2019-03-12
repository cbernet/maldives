from vocabulary import Vocabulary

import unittest
from collections import Counter
import pickle

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