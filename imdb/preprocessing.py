import glob
import os 
import pprint 

# persistency
import shelve

datadir = '/Users/cbernet/Datasets/MachineLearning/aclImdb'
train = 'train'
test = 'test'

categories = {'pos':1,
              'neg':0}

    
def load_reviews(train_or_test, category, stop=None):
    '''Load all reviews in a directory and return a dict.'''
    cwd = os.getcwd()
    dirname = '/'.join([datadir,train_or_test,category])
    os.chdir(dirname)
    files = glob.glob('*.txt')
    if stop:
        files = files[:stop]
    reviews = dict()
    for fname in files: 
        absfname = '/'.join([dirname,fname])
        root = os.path.splitext(fname)[0]
        num, rating = root.split('_')
        with open(fname) as ifile:
            review = ifile.read()
        revdata = dict( num=num,
                        rating=rating,
                        review=review)
        reviews[absfname] = revdata
    os.chdir(cwd)
    print('loaded {} reviews from {}'.format(len(reviews),dirname))
    label = '_'.join([train_or_test,category])
    return label, reviews

def preprocess(label, reviews):
    # set up natural language processing tools
    # imported here because it takes a long time
    import nltk
    nltk.download('punkt')
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words('english'))
    from bs4 import BeautifulSoup
    
    print('preprocessing {}'.format(label))
    for key, revdata in reviews.items():
        review = revdata['review']
        soup = BeautifulSoup(review, 'html.parser')
        review = soup.get_text()
        words = nltk.word_tokenize(review)
        words = [word.lower() for word in words]
        words = [word for word in words if word not in stop_words]
        revdata['preproc'] = words

if __name__ == '__main__':

    do_preprocess = False
    nreviews = 10
    if do_preprocess == True:
        all_samples = dict()    
        for train_test in ['train','test']:
            for pos_neg in ['pos', 'neg']:
                label, samples = load_reviews(train_test,pos_neg,stop=nreviews)
                preprocess(label, samples)
                all_samples[label] = samples
        sh = shelve.open('preprocessed')
        sh['data'] = all_samples
        sh.close()
    else: 
        sh = shelve.open('preprocessed')
        all_samples = sh['data']
        sh.close()
    for key, reviews in all_samples.items():
        print(key, len(reviews))
        a_review = next(iter(reviews.values()))
        pprint.pprint(a_review)
