import glob
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import keras
from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

def plot(impath):
    img = mpimg.imread(impath)
    plt.imshow(img)
    plt.show()

def plot_gen(generator):
    categ = ['cat','dog']
    nrows, ncols = 10, 5
    fig = plt.gcf()
    fig.set_size_inches(nrows*10, ncols*10)
    x, y = next(generator)
    for i, (img, y) in enumerate(zip(x,y)):
        subplot = plt.subplot(nrows, ncols, i+1)
        subplot.axis('Off')
        subplot.set_title(categ[int(y)])
        plt.imshow(img)
    plt.show()
    
train_dir = 'data/train'

dogs = sorted(glob.glob(train_dir+'dogs/dog.*.jpg'))
cats = sorted(glob.glob(train_dir+'cats/cat.*.jpg'))

dogs_y = np.zeros_like(dogs,dtype='d')
cats_y = np.ones_like(cats,dtype='d')

level_rescaler = ImageDataGenerator(rescale=1./255)
train_generator = level_rescaler.flow_from_directory(
    train_dir,
    target_size = (200,200),
    batch_size = 50,
    class_mode = 'binary',
    # save_to_dir = 'rescaled'
)

batch = next(train_generator)
batch[0].shape
batch[1].shape


