import json
import sys 
import os
import glob
import numpy as np
from collections import Counter

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def process_file(fname):
    '''process a review JSON lines file and count the words in all reviews.
    returns the counter, which will be used to find the most frequent words
    '''
    print(fname)
    ifile = open(fname)
    limit = options.nwords
    stop = options.lines
    all_data = np.zeros((min(file_len(fname),stop), limit+1),
                        dtype=np.int16)
    for i,line in enumerate(ifile): 
        if i%10000==0:
            print(i)        
        if i==stop:
            break        
        data = json.loads(line) 
        codes = data['text']  
        if not options.keep_unknown:
            codes = [code for code in codes if code!=1]
        stars = data['stars']
        all_data[i,0] = stars
        all_data[i,1:len(codes)+1] = codes[:limit]
    ifile.close()
    # print(len(all_stars), len(all_reviews
    print(fname,  'done')
    return all_data

def parse_args():
    from optparse import OptionParser        
    from base import setopts
    usage = "usage: %prog [options] <file_pattern>"
    parser = OptionParser(usage=usage)    
    setopts(parser)
    parser.add_option("-u", "--keep-unknown",
                      dest="keep_unknown", action="store_true", default=False,
                      help="keep unknown codes")   
    parser.add_option("-n", "--nwords",
                      dest="nwords", default=250, type=int,
                      help="max number of words, default 250")    
    (options, args) = parser.parse_args()    
    if len(args)!=1:
        parser.print_usage()
        sys.exit(1)
    pattern = args[0]
    return options, pattern

from base import setopts
    
if __name__ == '__main__':
    import os
    import pprint
    import h5py
    import parallelize

    options, pattern = parse_args()
    
    olddir = os.getcwd()
    os.chdir(options.datadir)
        
    fnames = glob.glob(pattern)
    
    nprocesses = len(fnames) if options.parallel else None
    results = parallelize.run(process_file, fnames, nprocesses)
    print('concatenating')
    data = np.concatenate(results)
    print(data) 
    
    ofname = 'data.h5'
    print('writing array to {}/{}'.format(ofname,'reviews'))
    h5 = h5py.File(ofname, 'w')
    h5.create_dataset('reviews', data=data) 
    h5.close()
    os.chdir(olddir)