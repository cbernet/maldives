
# coding: utf-8

# In[1]:


# the usual stuff: 
import matplotlib.pyplot as plt
import numpy as np
import keras

# get reproducible results
from numpy.random import seed
seed(0xdeadbeef)
from tensorflow import set_random_seed
set_random_seed(0xdeadbeef)

# needed to run on a mac: 
import os 
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


# In[2]:


import matplotlib.pyplot as plt

def plot_accuracy(history, miny=None):
  acc = history.history['acc']
  test_acc = history.history['val_acc']
  epochs = range(len(acc))
  plt.plot(epochs, acc)
  plt.plot(epochs, test_acc)
  if miny:
    plt.ylim(miny, 1.0)
  plt.title('accuracy') 
  plt.figure()


# In[3]:


import h5py
datadir = '/data2/cbernet/maldives/yelp_dataset/'
# datadir = './'
datafile = datadir+'data.h5'
h5 = h5py.File(datafile)
h5.keys()


# In[4]:


# load the vocabulary object from index.pck
import pickle 
with open(datadir+'index.pck', 'rb') as pckf: 
    vocab = pickle.load(pckf)


# In[5]:


data = h5['reviews']


# In[6]:


# the reviews
x = data[:, 4:]
# the stars, from which we will
# obtain the labels (see below)
stars = data[:,0]
# additional features we might consider:
useful = data[:,1]
cool = data[:,2]
funny = data[:,3]


# In[7]:


# first fill an array with zeros, 
# with the same shape as stars
y = np.zeros_like(stars)
# then write 1 if the number of stars is 4 or 5
y[stars>3.5] = 1
print(y, len(y))
print(stars, len(stars))


# In[14]:


n_test = 20000
n_train = 10000000
x_test = x[:n_test]
y_test = y[:n_test]
x_train = x[n_test:n_train+n_test]
y_train = y[n_test:n_train+n_test]


# In[17]:


model = keras.Sequential()
model.add(keras.layers.Embedding(len(vocab.words), 128, input_length=250))
model.add(keras.layers.LSTM(256))
model.add(keras.layers.Dense(1, activation='sigmoid'))
model.summary()
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])


# In[18]:


history = model.fit(x_train,
                    y_train,
                    epochs=5,
                    batch_size=100,
                    validation_data=(x_test, y_test),
                    verbose=1)


# In[13]:


plot_accuracy(history)

