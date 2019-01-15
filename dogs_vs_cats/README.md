# Dogs vs Cats 

## Introduction

* Goal of the exercise
* What will you learn 
* Prerequisites

## Get the dataset 

To download the input dataset,  we need to use the kaggle command, which is based on python 3. 

First, we create a python 3 environment for anaconda. We will only use it to get this dataset: 

```
conda create -n py3 python=3
conda activate py3
```

Install the kaggle command in this environment: 

```
pip install kaggle
```

Follow [these instructions](https://github.com/Kaggle/kaggle-api#api-credentials) to be able to log to kaggle with the kaggle command.

Download the dataset and inflate it: 

```
mkdir data 
cd data
kaggle competitions download -c dogs-vs-cats
unzip train.zip
mv train all
```

The input images are now available as: 

* dogs: `data/all/dog.*.jpg`
* cats: `data/all/cat.*.jpg`

Let's reorganize this files a bit, it will make our life easier later on: 

```
cd all
mkdir dogs 
mv dog.* dogs/
mkdir cats 
mv cat.* cats/ 
```

Now, you should have all dog pics in `data/all/dogs/`, and all cat pics in `data/all/cats/`.

Please have a look at some of these images to make sure that everything is as you expect. Always good to use a good old natural brain before trying to set up an artifiicial one. 

**explain splitting**

Now that we have retrieved the dataset, we will use python 2 for the rest of the tutorial. Please deactivate your python 3 environment: 

```
source deactivate
```

## Look at the data

Start ipython:

```
ipython 
```

Build the lists of files containing a dog or a cat image: 

```python
import glob
dogs = sorted(glob.glob('data/train/dogs/dog.*.jpg'))
cats = sorted(glob.glob('data/train/cats/cat.*.jpg'))
```

How many dogs and cats? 

```python
print len(dogs), len(cats)
```

Create a small image plotting function: 

```python
import matplotlib.image as mpimg
def plot(impath):
	img = mpimg.imread(impath)
	plt.imshow(img)
	plt.show()
```

And use it to plot the first dog pic: 

```python
plot(dogs[0])
```

Please have a look at a few other cat and dog pictures. 


## Image preprocessing 

As we have seen in the previous section, our cat and dog images come with different sizes and shapes. But the neural network must take a fixed number of input channels.

In this section, we will format the images into a suitable input to the neural network using the very convenient image preprocessing tools from keras. 

**explain rescaling, generator, ...** 

```python
from keras.preprocessing.image import ImageDataGenerator

level_rescaler = ImageDataGenerator(rescale=1./255)

train_generator = level_rescaler.flow_from_directory(
    train_dir,
    target_size = (200,200),
    batch_size = 50,
    class_mode = 'binary',
    # save_to_dir = 'rescaled'
)
```

The `train_generator` will provide batches of 50 images with the corresponding labels. Each image is forced to a size of 200x200 pixels. The colour levels of each image, originally between 0 and 255, are rescaled to be between 0 and 1.

Let's get the first batch to have a look: 

```python
x, y = next(train_generator)
print x.shape
print y.shape
print y
```

gives: 

```python
(50, 200, 200, 3)
(50,)
[1. 0. 0. 0. 1. 1. 1. 1. 1. 1. 0. 0. 1. 1. 1. 1. 0. 0. 1. 0. 0. 1. 0. 0.
 1. 0. 0. 1. 0. 0. 0. 1. 1. 0. 1. 0. 1. 1. 1. 1. 0. 0. 0. 0. 1. 1. 1. 0.
 0. 0.]
```

indeed, x contains 50 images with a size of 200x200 and 3 colour channels. y contains the corresponding 50 labels. 

Let's look at the first example in this batch: 

```python
print y[0]; plt.imshow(x[0]); plt.show()
```

**Garbage in, garbage out**

Feeding buggy inputs to a neural network is a guaranteed way to fail. For example, if we give a cat image and tell the network it's a dog, we will have a hard time training it to do anything useful. Also, we forced our images to a size of 200x200, but is a dog or a cat actually visible in the image after this operation? 

We could check our examples one by one as done just above, but I personally get very lazy when it comes to check things manually. So let's write a small function to help us a bit. 

**TODO : improve plotting function**

```python
def plot_gen(generator):
	nrows, ncols = 10, 5
	fig = plt.gcf()
	fig.set_size_inches(nrows*10, ncols*10)
	x, y = next(generator)
	for i, (img, y) in enumerate(zip(x,y)):
		subplot = plt.subplot(nrows, ncols, i+1)
		subplot.axis('Off')
		plt.imshow(img)
	plt.show()
```

Run it on your generator to display the next batch:

```python
plot_gen(train_generator)
```

## First try : a simple neural network

## Convolutional neural network

**network does not learn (starts too far from the minimum)**

Solution: initialize conv 2d layers (kernel and bias) with RandomUniform. Also tried lecun_uniform and the default, glorot_uniform. 

The last sigmoid layer is initialized with the default glorot_uniform. 

I think that the batch size shouldn't be too large? 

At the beginning, use a small number of images to work on this, overfitting is not a problem.

**overfitting**

Now using all pictures.

epoch 500 steps of 20 pics, so 10k pictures. But I have 22k. 
overfitting at epoch 30 already. 
letting it run to epoch 200 to look at the profile













