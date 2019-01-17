
from keras import layers, Model, optimizers

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
              optimizer=optimizers.RMSprop(lr=0.001),
              # optimizer=optimizers.Adam(lr=0.1),
              metrics=['acc'])

def fit_model(model, train_gen, val_gen, train_batch_size, val_batch_size, tensorboard):
    history = model.fit_generator(
        train_gen,
        steps_per_epoch=4000/train_batch_size,  
        epochs=100,
        validation_data=val_gen,
        validation_steps=1000/val_batch_size,  
        verbose=1,
        callbacks=[tensorboard]
    )
    return history 
    
