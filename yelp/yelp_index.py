# TODO:
import json
from collections import Counter

# removing stopwords that don't seem to carry information 
# about the quality of the review. 
# keeping 'not', for example, as negation is an important info.
# keeping ! which I think might be more frequent in negative reviews, and which is 
# typically used to make a statement stronger (in good or in bad). 
# the period, on the other hand, can probably be considered neutral
stopwords = set(['.','i','a','and','the','to', 'was', 'it', 'of', 'for', 'in', 'my', 
                 'that', 'so', 'do', 'our', 'the', 'and', ',', 'my', 'in', 'we', 'you', 
                 'are', 'is', 'be', 'me'])

def process_file(fname):
    '''process a file and counts the words in all reviews.
    returns the counter, which will be used to find the most frequent words
    '''
    print(fname)
    with open(fname) as ifile:
        counter = Counter()
        for i,line in enumerate(ifile): 
            data = json.loads(line) 
            # extract what we want
            words = data['text']               
            for word in words:
                if word in stopwords:
                    continue
                counter[word]+=1
            if i==stop:
                break
            if i%10000==0:
                print(i)
        return counter
    
def build_index(counter, n_most_common):
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
    reserved = ['<UNC>', '<PAD>']
    for res in reserved: 
        words.append(res)
        word_to_index[res] = i
        i += 1
    for word, dummy in most_common:
        words.append(word)
        word_to_index[word] = i
        i += 1 
    return words, word_to_index
        
    
if __name__ == '__main__':
    import os
    import glob    
    import pprint
    import shelve
    from multiprocessing import Pool, Process, Queue
    
    datadir = os.path.expanduser('~/Datasets/MachineLearning/yelp_dataset/')
    olddir = os.getcwd()
    os.chdir(datadir)

    fnames = glob.glob('xa?_tok.json')
    # read the first entries
    # set to -1 to process everything
    stop = -1
    # limit vocabulary to the most common words 
    n_most_common = 10000
    # large number, so that multiprocessing 
    # can finalize its tasks
    timeout = 10000
    # use multiprocessing? 
    parallel = True
    
    print(fnames)
    
    counter = Counter()
    
    full_counter = Counter()
    if not parallel:
        for fname in fnames:
            full_counter = process_file(fname)
    else:
        q = Queue()
        with Pool(processes=len(fnames)) as pool:
            results = []
            # the following runs asynchronously
            for fname in fnames: 
                results.append( pool.apply_async(process_file, [fname]) )
            # collapsing the results after all processes are done
            for res in results:
                counter = res.get(timeout=timeout)
                full_counter.update(counter)
                pprint.pprint(counter.most_common(10))
    pprint.pprint(full_counter.most_common(50))
    
    words, index = build_index(full_counter, n_most_common)

    with shelve.open('index') as sh:
        sh['words'] = words
        sh['index'] = index
    
    os.chdir(olddir)    