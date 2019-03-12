import json
import os
from collections import Counter

def output_fname(input_fname):
    return  input_fname.split('_')[0] + '_enc.json'

def process_file(fname, options, vocabulary):
    '''process a review JSON lines file and count the words in all reviews.
    returns the counter, which will be used to find the most frequent words
    '''
    print(fname)
    ofname = output_fname(fname)  
    ifile = open(fname) 
    ofile = open(ofname,'w')
    for i,line in enumerate(ifile): 
        if i==options.lines:
            break
        if i%10000==0:
            print(i)        
        data = json.loads(line) 
        words = data['text']     
        codes = vocabulary.encode(words)
        data['text'] = codes
        line = json.dumps(data)
        ofile.write(line+'\n')        
    ifile.close()
    ofile.close()
    
def parse_args():
    from optparse import OptionParser        
    from base import setopts
    usage = "usage: %prog [options] <file_pattern>"
    parser = OptionParser(usage=usage)    
    setopts(parser)
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
    import shelve
    from vocabulary import Vocabulary
    import parallelize
    
    options, pattern = parse_args()
    
    olddir = os.getcwd()
    os.chdir(options.datadir)

    vocabulary = Vocabulary.load('index')
        
    fnames = glob.glob(pattern)
    print(fnames)
    
    nprocesses = len(fnames) if options.parallel else None
    results = parallelize.run(process_file, fnames, nprocesses, 
                              options, vocabulary)
    
