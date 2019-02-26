import sys
import os 

def setopts(parser):
    parser.add_option("-l", "--lines",
                      dest="lines", default=sys.maxsize, type=int,
                      help="max number of lines, default all")
    parser.add_option("-n", "--nwords",
                      dest="nwords", default=500, type=int,
                      help="max number of words, default 500")
    parser.add_option("-p", "--parallel",
                      dest="parallel", action="store_true", default=False, 
                      help="parallel mode")
    parser.add_option("-d", "--datadir",
                      dest="datadir", 
                      default=os.path.expanduser('~/Datasets/MachineLearning/yelp_dataset/'),
                      help="data directory")
