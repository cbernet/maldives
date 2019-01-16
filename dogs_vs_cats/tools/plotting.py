import matplotlib.pyplot as plt 
import matplotlib.image as mpimg

def plot(impath):
    img = mpimg.imread(impath)
    plt.imshow(img)
    plt.show()

categories = ['cat', 'dog']
    
def plot_pred(x, y, preds):
    nrows, ncols = 4, 5
    fig = plt.gcf()
    for i, (img, target, prediction) in enumerate(zip(x, y, preds)):
        subplot = plt.subplot(nrows, ncols, i+1)
        subplot.axis('Off')
        category = categories[int(target)]
        subplot.set_title('{category} {pred:5.2f}'.format(category=category,
                                                          pred=prediction[0]))
        plt.imshow(img)
    plt.show()
                                          


def plot_gen(generator):
    nrows, ncols = 10, 5
    fig = plt.gcf()
    fig.set_size_inches(nrows*10, ncols*10)
    x, y = next(generator)
    for i, (img, y) in enumerate(zip(x,y)):
        subplot = plt.subplot(nrows, ncols, i+1)
        subplot.axis('Off')
        subplot.set_title(categories[int(y)])
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
    
