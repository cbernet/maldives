# TODO:
# - disk size + 72%. can we improve by storing to another format, h5? 
# - add multiprocessing
# - think about next steps 

import json

import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from nltk.probability import FreqDist    

def preprocess(text):
    # set up natural language processing tools
    # imported here because it takes a long time
    words = nltk.word_tokenize(text)
    words = [word.lower() for word in words]
    # i think stopwords might be useful with lstm.. e.g. negations
    # words = [word for word in words if word not in stop_words]
    return words

def process_file(fname):
    print('opening', fname)
    ofname = fname + '_tok.json'
    ifile = open(fname)
    ofile = open(ofname,'w')
    for i, line in enumerate(ifile):
        if i%1000 == 0:
            print(i) 
        if i==stop:
            break        
        # convert the json on this line to a dict
        data = json.loads(line) 
        # extract what we want
        text = data['text']   
        words = preprocess(text)
        data['text'] = words
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
    from multiprocessing import Pool
    
    options, pattern = parse_args()
    olddir = os.getcwd()    
    os.chdir(datadir)

    fnames = glob.glob(pattern)
       
    nprocesses = len(fnames) if options.parallel else None
    results = parallelize.run(process_file, fnames, nprocesses)
            
    os.chdir(olddir)    