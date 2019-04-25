import numpy as np
import keras

# get reproducible results
from numpy.random import seed
seed(0xdeadbeef)
from tensorflow import set_random_seed
set_random_seed(0xdeadbeef)

import h5py
datadir = '/data2/cbernet/maldives/yelp_dataset/'
datafile = datadir+'data.h5'
h5 = h5py.File(datafile)
h5.keys()

data = h5['reviews']

import pickle
with open(datadir+'index.pck', 'rb') as pckf:
    vocab = pickle.load(pckf)
    

# the reviews
x = data[:, 4:]
# the stars, from which we will
# obtain the labels (see below)
stars = data[:,0]
# additional features we might consider:
useful = data[:,1]
cool = data[:,2]
funny = data[:,3]

# first fill an array with zeros,
# with the same shape as stars
y = np.zeros_like(stars)
# then write 1 if the number of stars is 4 or 5
y[stars>3.5] = 1
print(y, len(y))
print(stars, len(stars))

n_test = 20000
n_train = int(1e5)
x_test = x[:n_test]
y_test = y[:n_test]
x_train = x[n_test:n_test+n_train]
y_train = y[n_test:n_test+n_train]

model = keras.Sequential()

model.add(keras.layers.Embedding(len(vocab.words), 64, input_length=250))
model.add(keras.layers.Conv1D(filters=16, kernel_size=3, padding='same', activation='relu'))
model.add(keras.layers.MaxPooling1D(pool_size=2))
model.add(keras.layers.Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
model.add(keras.layers.MaxPooling1D(pool_size=2))
model.add(keras.layers.Conv1D(filters=64, kernel_size=3, padding='same', activation='relu'))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dropout(rate=0.5))
model.add(keras.layers.Dense(100, activation='relu'))
model.add(keras.layers.Dense(1, activation='sigmoid'))
model.summary()

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(x_train,
                    y_train,
                    epochs=4,
                    batch_size=1000,
                    validation_data=(x_test, y_test),
                    verbose=1)
