import json
import sys 
import os
import glob
import numpy as np
import h5py

def file_len(fname):
    '''Counts the number of lines in the file with name fname
    '''
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def process_file(fname, options):
    '''process a review JSON lines file 
    and return a numpy array with the data.
    '''
    print(fname)
    ifile = open(fname)
    # limit on the number of words in reviews
    limit = options.nwords
    stop = options.lines
    # creating the numpy array in advance 
    # so that we don't have to resize it later.
    # the total size along the second axis is limit+4 
    # to leave four additional slots for 
    # the rating, useful, funny, cool   
    # all cells are initialized to 0 so that the padding
    # is automatically done. 
    n_features = 4
    all_data = np.zeros((min(file_len(fname),stop), limit+n_features),
                        dtype=np.int16)
    for i,line in enumerate(ifile): 
        if i%10000==0:
            print(i)        
        if i==stop:
            break        
        data = json.loads(line) 
        codes = data['text']  
        # we can decide to keep the unknown words (code=1)
        # or just to drop them (default).
        if not options.keep_unknown:
            codes = [code for code in codes if code!=1]
        # store the rating in the 1st column
        all_data[i,0] = data['stars']
        all_data[i,1] = data['useful']
        all_data[i,2] = data['funny']
        all_data[i,3] = data['cool']
        # store the encoded words afterwards 
        # the review is truncated to limit.
        truncated = codes[:limit]
        all_data[i,n_features:len(truncated)+n_features] = truncated
    ifile.close()
    # print(len(all_stars), len(all_reviews
    print(fname,  'done')
    return all_data

def finalize(results):
    # concatenating the numpy arrays for all files
    print('concatenating')
    data = np.concatenate(results)
    print(data) 
    # saving the full numpy array to an hdf5 file
    ofname = 'data.h5'
    print('writing array to {}/{}'.format(ofname,'reviews'))
    h5 = h5py.File(ofname, 'w')
    h5.create_dataset('reviews', data=data) 
    h5.close()    

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
    
if __name__ == '__main__':
    import os
    import pprint
    import parallelize

    options, pattern = parse_args()
    
    olddir = os.getcwd()
    os.chdir(options.datadir)
        
    fnames = glob.glob(pattern)
    
    nprocesses = len(fnames) if options.parallel else None
    results = parallelize.run(process_file, fnames, nprocesses, options)
    finalize(results)
    os.chdir(olddir)
