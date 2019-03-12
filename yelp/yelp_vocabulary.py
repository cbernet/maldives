'''Build the vocabulary for the yelp dataset'''

import json
from collections import Counter

# stop words are words that occur very frequently,
# and that don't seem to carry information 
# about the quality of the review. 
# we decide to keep 'not', for example, as negation is an important info.
# I also keep ! which I think might be more frequent in negative reviews, and which is 
# typically used to make a statement stronger (in good or in bad). 
# the period, on the other hand, can probably be considered neutral
# this could have been done at a later stage as well, 
# but we can do it here as this stage is fast 
stopwords = set(['.','i','a','and','the','to', 'was', 'it', 'of', 'for', 'in', 'my', 
                 'that', 'so', 'do', 'our', 'the', 'and', ',', 'my', 'in', 'we', 'you', 
                 'are', 'is', 'be', 'me'])

def process_file(fname, options):
    '''process a review JSLON lines file and count the occurence 
    of each words in all reviews.
    returns the counter, which will be used to find the most frequent words
    '''
    print(fname)
    with open(fname) as ifile:
        counter = Counter()
        for i,line in enumerate(ifile):
            if i==options.lines:
                break
            if i%10000==0:
                print(i)            
            data = json.loads(line) 
            # extract what we want
            words = data['text']               
            for word in words:
                if word in stopwords:
                    continue
                counter[word]+=1
        return counter

def parse_args():
    from optparse import OptionParser        
    from base import setopts
    usage = "usage: %prog [options] <file_pattern>"
    parser = OptionParser(usage=usage)    
    setopts(parser)
    parser.add_option("-n", "--nwords",
                      dest="nwords", default=20000, type=int,
                      help="max number of words in vocabulary, default 20000")
    (options, args) = parser.parse_args()    
    if len(args)!=1:
        parser.print_usage()
        sys.exit(1)
    pattern = args[0]
    return options, pattern

if __name__ == '__main__':
    import os
    import glob    
    import pprint
    from vocabulary import Vocabulary
    import parallelize


    options, pattern = parse_args()
    
    olddir = os.getcwd()
    os.chdir(options.datadir)

    fnames = glob.glob(pattern)
       
    nprocesses = len(fnames) if options.parallel else None
    results = parallelize.run(process_file, fnames, nprocesses, options)

    full_counter = Counter()
    for counter in results:
        full_counter.update(counter)

    vocabulary = Vocabulary(full_counter, n_most_common=options.nwords)
    vocabulary.save('index')
    
    pprint.pprint(full_counter.most_common(200))
    print(len(full_counter))
    print(vocabulary)
    os.chdir(olddir)    