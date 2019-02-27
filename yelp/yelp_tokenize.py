'''Tokenize a JSON lines dataset with nltk
'''

import json

import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
# stop_words = set(stopwords.words('english'))
from nltk.probability import FreqDist    

def process_file(fname):
    '''tokenize data in file fname. 
    The output is written to fname_tok.json
    '''
    print('opening', fname)
    ofname = fname + '_tok.json'
    ifile = open(fname)
    ofile = open(ofname,'w')
    for i, line in enumerate(ifile):
        if i%1000 == 0:
            print(i) 
        if i==options.lines:
            break        
        # convert the json on this line to a dict
        data = json.loads(line) 
        # extract the review text
        text = data['text']
        # tokenize
        words = nltk.word_tokenize(text)
        # convert all words to lower case 
        words = [word.lower() for word in words]
        # updating JSON and writing to output file
        data['text'] = words
        line = json.dumps(data)
        ofile.write(line+'\n')
    ifile.close()
    ofile.close()

def parse_args():
    '''Parse command line arguments.
    See base.setopts for more information
    '''
    from optparse import OptionParser        
    from base import setopts
    usage = "usage: %prog [options] <file_pattern>"
    parser = OptionParser(usage=usage)    
    setopts(parser)
    (options, args) = parser.parse_args()    
    if len(args)!=1:
        parser.print_usage()
        sys.exit(1)
    # pattern should match the files you want to process, 
    # e.g. 'xa*'
    pattern = args[0]
    return options, pattern

if __name__ == '__main__':
    import os
    import glob
    import parallelize
    from multiprocessing import Pool
    
    options, pattern = parse_args()
    olddir = os.getcwd()    
    os.chdir(options.datadir)

    fnames = glob.glob(pattern)
       
    nprocesses = len(fnames) if options.parallel else None
    results = parallelize.run(process_file, fnames, nprocesses)
            
    os.chdir(olddir)    

