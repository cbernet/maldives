
# load the data -------------------------
import tensorflow as tf
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# preprocessing: -------------------------

# normalizing the greyscale to 1 
import numpy as np
x_train = x_train/255.
x_test = x_test/255.

# reshaping for keras
kx_train = x_train.reshape(len(x_train),28,28,1)
kx_test = x_test.reshape(len(x_test),28,28,1)


# one-hot encoding: 
# turn the category label (0, 1, ... or 9)
# to a binary array of length 10, e.g. 
# 2 -> [0,1,0,...0]

y_train = tf.keras.utils.to_categorical(y_train, 10)
y_test = tf.keras.utils.to_categorical(y_test, 10)

# build the deep neural net -------------

from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.optimizers import RMSprop

model = models.Sequential()
model.add( layers.Conv2D(16, 4, input_shape=(28,28,1), activation='relu') )
model.add( layers.MaxPooling2D(2) )
model.add( layers.Conv2D(32, 4, activation='relu') )
model.add( layers.MaxPooling2D(2) )
model.add( layers.Flatten() )
model.add( layers.Dropout(0.4) )
model.add( layers.Dense(100, activation='relu') )
model.add( layers.Dense(10, activation='softmax') )
model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['acc'])

history = model.fit(kx_train, y_train, validation_data=(kx_test,y_test),
                    batch_size=200, epochs=40)

model.save('model.h5')


