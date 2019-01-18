
from keras.preprocessing.image import ImageDataGenerator


data_dir = '/data2/cbernet/maldives/dogs_vs_cats/data'
train_dir = data_dir+'/train'
validation_dir = data_dir+'/validation'

train_rescaler = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
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

