import json
from collections import Counter

def process_file(fname):
    '''process a review JSON lines file and count the words in all reviews.
    returns the counter, which will be used to find the most frequent words
    '''
    print(fname)
    ofname = fname.split('_')[0] + '_enc.json'
    ifile = open(fname) 
    ofile = open(ofname,'w')
    for i,line in enumerate(ifile): 
        data = json.loads(line) 
        words = data['text']     
        codes = index.encode(words)
        data['text'] = codes
        line = json.dumps(data)
        ofile.write(line+'\n')        
        if i==stop:
            break
        if i%10000==0:
            print(i)
    ifile.close()
    ofile.close()
    
    
if __name__ == '__main__':
    import os
    import glob    
    import pprint
    import shelve
    from index import Index
    import parallelize
    
    datadir = os.path.expanduser('~/Datasets/MachineLearning/yelp_dataset/')
    # read the first entries
    # set to -1 to process everything
    stop = -1
    # use multiprocessing? 
    parallel = True    
    
    olddir = os.getcwd()
    os.chdir(datadir)

    index = Index(dbfname='index')
        
    fnames = glob.glob('xa?_tok.json')
    print(fnames)
    
    nprocesses = len(fnames) if parallel else 1
    results = parallelize.run(process_file, fnames, nprocesses)
    
