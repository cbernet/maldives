# TODO:
# - disk size + 72%. can we improve by storing to another format, h5? 
# - add multiprocessing
# - think about next steps 

import json

import nltk
from nltk.corpus import stopwords
# stop_words = set(stopwords.words('english'))
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
        # convert the json on this line to a dict
        data = json.loads(line) 
        # extract what we want
        text = data['text']   
        words = preprocess(text)
        data['text'] = words
        line = json.dumps(data)
        ofile.write(line+'\n')
        if i%1000 == 0:
            print(i) 
        if i==stop:
            break
    ifile.close()
    ofile.close()


    
if __name__ == '__main__':
    import os
    import glob    
    from multiprocessing import Pool
    
    datadir = os.path.expanduser('~/Datasets/MachineLearning/yelp_dataset/')
    os.chdir(datadir)

    fnames = glob.glob('xa?')
    # read the first entries
    # set to -1 to process everything
    stop = -1
    parallel = True
    print(fnames)
    
    if not parallel:
        for fname in fnames:
            process_file(fname)
    else:
        with Pool(10) as p: 
            p.map(process_file,fnames)
