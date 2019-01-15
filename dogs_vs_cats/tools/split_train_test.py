
import sys
import os
import shutil
import random
import numpy as np

data_dir = sys.argv[1]
train_fraction = float(sys.argv[2])

all_dir = data_dir + '/all'
train_dir = data_dir + '/train'
validation_dir = data_dir + '/validation'

def prepare_dir(path, categories):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    for categ in categories:
        os.mkdir( '/'.join([path,categ]) )

def split_samples(all_dir, dest_dirs, fractions):
    dest_dirs = np.array(dest_dirs)
    assert(len(dest_dirs)==len(fractions))
    for categ in categories:
        src_dir = '/'.join([all_dir,categ])
        for img in os.listdir(src_dir):
            dest_mask = np.random.multinomial(1, fractions)
            dest_dir = dest_dirs[dest_mask==1]
            src_path = '/'.join([src_dir, img])
            dest_path = '/'.join([dest_dir[0],categ,os.path.basename(img)])
            shutil.copyfile(src_path, dest_path)
    
categories = os.listdir(all_dir)
prepare_dir(train_dir, categories)
prepare_dir(validation_dir, categories)

split_samples(all_dir, [train_dir, validation_dir], [train_fraction, 1-train_fraction])


        


