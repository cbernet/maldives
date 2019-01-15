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


def plot_history(history):
    acc = history.history['acc']
    val_acc = history.history['val_acc']

    # Retrieve a list of list results on training and test data
    # sets for each training epoch
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    # Get number of epochs
    epochs = range(len(acc))

    # Plot training and validation accuracy per epoch
    plt.plot(epochs, acc)
    plt.plot(epochs, val_acc)
    plt.title('Training and validation accuracy')

    plt.figure()

    # Plot training and validation loss per epoch
    plt.plot(epochs, loss)
    plt.plot(epochs, val_loss)
    plt.title('Training and validation loss')
    plt.show()
    
train_dir = 'data/train'
validation_dir = 'data/validation'

dogs = sorted(glob.glob(train_dir+'dogs/dog.*.jpg'))
cats = sorted(glob.glob(train_dir+'cats/cat.*.jpg'))

dogs_y = np.zeros_like(dogs,dtype='d')
cats_y = np.ones_like(cats,dtype='d')

train_rescaler = ImageDataGenerator(
    rescale=1./255,
#    rotation_range=40,
#    width_shift_range=0.2,
#    height_shift_range=0.2,
#    shear_range=0.2,
#    zoom_range=0.2,
#    horizontal_flip=True,
)
test_rescaler = ImageDataGenerator(rescale=1./255)

train_batch_size = 20
val_batch_size = 20

train_generator = train_rescaler.flow_from_directory(
    train_dir,
    target_size = (200,200),
    batch_size = train_batch_size,
    class_mode = 'binary',
    # save_to_dir = 'rescaled'
)

validation_generator = test_rescaler.flow_from_directory(
    validation_dir,
    target_size = (200,200),
    batch_size = val_batch_size,
    class_mode = 'binary',
    # save_to_dir = 'rescaled'
)


# batch = next(train_generator)
# batch[0].shape
# batch[1].shape

# MLP
# model = keras.Sequential()
# model.add( keras.layers.Reshape(input_shape=(200,200,3), target_shape=(200*200*3,)) )
# model.add( keras.layers.Dense(256, input_shape=(200*200*3,), activation='relu') )
# model.add( keras.layers.Dense(1, activation='sigmoid') )

from keras import layers, Model

img_input = layers.Input(shape=(200, 200, 3))

#initializers
conv_ini = 'RandomUniform'

# First convolution extracts 16 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(24, 5, activation='relu',
                  kernel_initializer=conv_ini, bias_initializer=conv_ini)(img_input)
x = layers.MaxPooling2D(2)(x)

# Second convolution extracts 32 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(48, 5, activation='relu',
                  kernel_initializer=conv_ini, bias_initializer=conv_ini)(x)
x = layers.MaxPooling2D(2)(x)

# Third convolution extracts 64 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(96, 5, activation='relu',
                  kernel_initializer=conv_ini, bias_initializer=conv_ini)(x)
x = layers.MaxPooling2D(2)(x)

# Flatten feature map to a 1-dim tensor so we can add fully connected layers
x = layers.Flatten()(x)

# Create a fully connected layer with ReLU activation and 512 hidden units
x = layers.Dropout(0.5)(x)
x = layers.Dense(512, activation='relu')(x)
# x = layers.Dense(1024, activation='relu')(x)
# x = layers.Dense(128, activation='relu')(x)

# Create output layer with a single node and sigmoid activation
output = layers.Dense(1, activation='sigmoid')(x)

# Create model:
# input = input feature map
# output = input feature map + stacked convolution/maxpooling layers + fully
# connected layer + sigmoid output layer
model = Model(img_input, output)

model.compile(loss='binary_crossentropy',
              optimizer=keras.optimizers.RMSprop(lr=0.001),
              # optimizer=keras.optimizers.Adam(lr=0.1),
              metrics=['acc'])

model.summary()

if 1:
    history = model.fit_generator(
        train_generator,
        steps_per_epoch=4000/train_batch_size,  
        epochs=50,
        validation_data=validation_generator,
        validation_steps=1000/val_batch_size,  
        verbose=1)
    
