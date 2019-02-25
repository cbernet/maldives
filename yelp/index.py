import shelve
import pprint


class Index(object): 
    
    def __init__(self, counter=None, dbfname=None, n_most_common=10000):
        '''Constructor. Either provide a counter or the path to a shelve db'''
        if not counter and not dbfname: 
            raise ValueError('provide either a counter or a db filename')   
        if counter: 
            self.words, self.index = self._build_index(counter, n_most_common)
        else:
            with shelve.open(dbfname) as sh:
                self.words = sh['words']
                self.index = sh['index']
                
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
        for tag in ['<UNK>', '<PAD>']: 
            words.append(tag)
            word_to_index[tag] = i
            i += 1
        for word, dummy in most_common:
            words.append(word)
            word_to_index[word] = i
            i += 1 
        return words, word_to_index
            
    def save(self, dbfname): 
        '''Save words, index, stopwords to a shelve'''
        with shelve.open('index') as sh:
            sh['words'] = self.words
            sh['index'] = self.index
        
    def decode(self, list_of_codes):
        '''print the sentence corresponding to a list of codes'''
        return ' '.join(self.words[i] for i in list_of_codes)
    
    def encode(self, list_of_words): 
        '''return the list of codes corresponding to a list of words'''
        return [self.index.get(word, 0) for word in list_of_words]
             
