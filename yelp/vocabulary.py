'''Vocabulary'''

import pickle
import pprint


class Vocabulary(object): 
    '''Vocabulary'''
    
    def __init__(self, counter=None, n_most_common=10000):
        '''Constructor. Either provide a counter to build the vocabulary 
        or the path to a shelve db to load a pre-existing vocabulary.'''
        self.n_most_common = n_most_common
        if not counter and not dbfname: 
            raise ValueError('provide either a counter or a db filename')   
        if counter: 
            self.words, self.index = self._build_index(counter, n_most_common)
        else:
            self.words = None
            self.index = None
            
    def _build_index(self, counter, n_most_common):
        '''takes the most frequent words in common. 
        returns: list_of_words, index 
        
        the list of words needs to be ordered as a word
        will be encoded later on by its position in the list.
        de-encoding an integer to its corresponding word then can be done 
        with random access.
       
        the index is a dictionary : (word, index)
        it will provide random access to the index corresponding to a word
        during encoding.
        '''
        most_common = counter.most_common(n_most_common)
        words = []
        word_to_index = dict()
        i = 0
        # reserved :
        for tag in ['<PAD>','<UNK>']: 
            words.append(tag)
            word_to_index[tag] = i
            i += 1
        for word, dummy in most_common:
            words.append(word)
            word_to_index[word] = i
            i += 1 
        return words, word_to_index
            
    def save(self, fname): 
        '''Save words, index, stopwords to a shelve'''
        with open(fname + '.pck', 'wb') as pckfile:
            pickle.dump(self, pckfile)
    
    @classmethod
    def load(cls, fname):
        '''load a vocabulary from a pickle file 
        and return the vocabulary object'''
        with open(fname + '.pck', 'rb') as pckfile:
            return pickle.load(pckfile)        
        
    def decode(self, list_of_codes):
        '''print the sentence corresponding to a list of codes'''
        return [self.words[i] for i in list_of_codes]
    
    def encode(self, list_of_words): 
        '''return the list of codes corresponding to a list of words'''
        return [self.index.get(word, 1) for word in list_of_words]
             
    def __str__(self):
        return pprint.pformat(self.words[:20])
