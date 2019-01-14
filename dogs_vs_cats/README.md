# Dogs vs Cats 

## Get the dataset 

To download the input dataset, you need to use the kaggle command, which is based on python 3. 

First create a python 3 environment for anaconda. We will only use it to get this dataset: 

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
```

The input images are now available as: 

* dogs: `data/train/dog.*.jpg`
* cats: `data/train/cat.*.jpg`

Please have a look at some of these images to make sure that everything is as you expect. Always good to use a good old natural brain before trying to set up an artifiicial one. 

Now that we have retrieved the dataset, we will use python 2 for the rest of the tutorial. Please deactivate your python 3 environment: 

```
source deactivate
```

## Look at the data

Start ipython:

```
ipython --pylab
```

Build the lists of files containing a dog or a cat image: 

```
import glob
dogs = sorted(glob.glob('data/train/dog.*.jpg'))
cats = sorted(glob.glob('data/train/cat.*.jpg'))
```

How many dogs and cats? 

```
print len(dogs), len(cats)
```

Create a small image plotting function: 

```
import matplotlib.image as mpimg
def plot(impath):
	img = mpimg.imread(impath)
	plt.imshow(img)
	plt.show()
```

And use it to plot the first dog pic: 

```
plot(dogs[0])
```

Please have a look at a few other cat and dog pictures. 


## Image preprocessing 

As we have seen in the previous section, our cat and dog images come with different sizes and shapes. But the neural network must take a fixed number of input variables.  



