#!/usr/bin/python3

import numpy, os, progressbar, tensorflow
import tensorflow.keras as keras
from dablog.util import Codebook

if False:
    gpus = tensorflow.config.experimental.list_physical_devices ('GPU')
    tensorflow.config.experimental.set_visible_devices (devices=gpus, device_type='GPU')
    for i in range (0, len (gpus)): tensorflow.config.experimental.set_memory_growth (gpus [i], True)

class Word2VecMimickEmbedding (object):

    def __init__ (self, input_size, output_size, filepath=None, verbose=True):
        self.input_size = input_size
        self.output_size = output_size
        self.filepath = filepath
        self.verbose=verbose
        self.epochs = 64 
        self.batchsize = 32
        self.model = None

    def buildModel (self):
        self.word_input = keras.layers.Input (shape=(None, self.input_size), name='Input')
        self.nn = keras.models.Sequential (name='Bi_RNN')
        self.nn.add (keras.layers.Bidirectional (keras.layers.LSTM (self.input_size), merge_mode='concat', name='Bi_LSTM'))
        self.nn.add (keras.layers.Dense (self.input_size, activation='relu', name='Dense_1'))
        self.nn.add (keras.layers.Dense (self.output_size, activation=None, name='Dense_2'))
        self.model = keras.models.Model (inputs=self.word_input, outputs=self.nn (self.word_input))
        self.model.compile (loss=self.mse_loss, optimizer='adam')
        if self.verbose: self.model.summary () 
        if self.verbose: self.nn.summary ()

    def train (self, X, Y):
        return self.fit (X, Y)

    def fit (self, X, Y):
        if self.model is None: 
            self.buildModel ()
        ret = self.model.fit (X, Y, shuffle=True, verbose=self.verbose, batch_size=self.batchsize, epochs=self.epochs)
        if self.filepath is not None: self.save ()
        return ret

    def evaluate (self, X):
        return self.predict (testset)

    def predict (self, X):
        if self.model is None: self.load ()
        return self.model.predict (X, batch_size=self.batchsize, verbose=False)

    @staticmethod
    def mse_loss (y_true, y_pred):
        return tensorflow.reduce_mean (tensorflow.reduce_sum (tensorflow.square (y_pred - y_true), axis=-1), axis=-1)

    def save (self, filepath=None):
        if filepath is None: filepath = self.filepath
        if filepath is not None:
            filepath = os.path.join (filepath, 'mimick.h5')
            self.model.save (filepath)

    def load (self, filepath=None):
        if filepath is None: filepath = self.filepath
        if filepath is not None:
            filepath = os.path.join (filepath, 'mimick.h5')
            custom_objects = {'mse_loss': self.mse_loss}
            self.model = keras.models.load_model (filepath, custom_objects=custom_objects)

