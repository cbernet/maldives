import keras
import matplotlib.pyplot as plt
import numpy as np
from plotting import plot_gen, plot_history, plot_pred
from dataset import train_generator, validation_generator, val_batch_size, train_batch_size
# from model import model, fit_model
# print model.summary()
from time import time
from keras.callbacks import TensorBoard


if __name__ == '__main__':
    import sys
    from optparse import OptionParser
    import imp
    
    usage = '''usage: %prog <model> 
    
    training mode: <model> should be the path to a python module defining the model
    loading mode : <model> should be the path to an h5 file containing the trained model 
'''
    parser = OptionParser(usage=usage)

    parser.add_option("-v", "--verbose", dest="verbose",
                      action='store_true',
                      default=False,
                      help='verbose mode')
    options, args = parser.parse_args()

    if len(args)!=1:
        print parser.usage
        sys.exit(1)

    model = None
    fit_model = None
    model_path = args[0]
    mode = None
    if model_path.endswith('.py'):
        print 'training', model_path
        with open(model_path) as ifile:
            mode = 'fit'
            mod = imp.load_source('mod', model_path, ifile)
            model = mod.model
            fit_model = mod.fit_model
    elif model_path.endswith('h5'):
        mode = 'load'
        print 'loading', model_path
        model = keras.models.load_model(model_path)

    if mode == 'fit':
        tensorboard = TensorBoard(log_dir="logs/{}".format(time()))
        fit_model(model, train_generator, validation_generator, train_batch_size, val_batch_size, tensorboard)
        
    model.summary()

    # b = next(validation_generator)
    # p = model.predict_on_batch(b[0])
    # plot_pred(b[0], b[1], p)
