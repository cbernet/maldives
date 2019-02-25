import json
from collections import Counter

# removing stopwords that don't seem to carry information 
# about the quality of the review. 
# keeping 'not', for example, as negation is an important info.
# keeping ! which I think might be more frequent in negative reviews, and which is 
# typically used to make a statement stronger (in good or in bad). 
# the period, on the other hand, can probably be considered neutral
# this could have been done at a later stage as well, 
# but that's not important as this stage is fast 
stopwords = set(['.','i','a','and','the','to', 'was', 'it', 'of', 'for', 'in', 'my', 
                 'that', 'so', 'do', 'our', 'the', 'and', ',', 'my', 'in', 'we', 'you', 
                 'are', 'is', 'be', 'me'])

def process_file(fname):
    '''process a review JSLON lines file and count the words in all reviews.
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

if __name__ == '__main__':
    import os
    import glob    
    from index import Index
    import parallelize

    
    datadir = os.path.expanduser('~/Datasets/MachineLearning/yelp_dataset/')
    # read the first entries
    # set to -1 to process everything
    stop = -1
    # limit vocabulary to the most common words 
    n_most_common = 10000
    # use multiprocessing? 
    parallel = True
    
    olddir = os.getcwd()
    os.chdir(datadir)

    
    fnames = glob.glob('xa?_tok.json')
    print(fnames)
       
    nprocesses = len(fnames) if parallel else 1
    results = parallelize.run(process_file, fnames, nprocesses)

    full_counter = Counter()
    for counter in results:
        full_counter.update(counter)

    index = Index(full_counter, n_most_common)
    index.save('index')

    os.chdir(olddir)    