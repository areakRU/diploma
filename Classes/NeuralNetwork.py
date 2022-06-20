from numpy import ndarray
from tensorflow import keras
from keras.layers import Conv1D
from keras.layers import MaxPooling1D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Reshape
from keras.layers import InputLayer
from keras.layers import Flatten
from keras.layers import AveragePooling1D
from keras.layers import GlobalMaxPooling1D
from keras.layers import BatchNormalization
from keras.optimizers import adam_v2
from keras.models import Sequential
import numpy as np

class Network:
    def __init__(self, PATH = r'NeuralNetwork\saved_model.hdf5'):
        N_classes = 6

        self.model = Sequential()
        self.model.add(InputLayer(input_shape=(2000, )))
        self.model.add(Reshape((2000,1),input_shape=(2000,)))
        self.model.add(BatchNormalization())
        self.model.add(Conv1D(25,40, activation='elu',padding='same', strides=2)) # количество фильтров, длинна фильтра 'relu' #25
        self.model.add(Conv1D(25,20, activation='elu',padding='same',name = 'style'))#25
        self.model.add(Conv1D(20,20, activation='elu',padding='same', strides=2))#25
        self.model.add(Conv1D(25,20, activation='elu',padding='same'))#25
        self.model.add(BatchNormalization())
        self.model.add(MaxPooling1D(2))
        self.model.add(Conv1D(20,20, activation='elu',padding='same'))#25
        self.model.add(Conv1D(40,20, activation='elu',padding='same'))#40
        self.model.add(Conv1D(100,20, activation='elu',padding='same'))#100
        self.model.add(Dropout(0.5))
        self.model.add(BatchNormalization())
        self.model.add(MaxPooling1D(2))
        self.model.add(GlobalMaxPooling1D(name = 'flatt'))
        self.model.add(Dense(N_classes, activation='softmax'))

        opt = keras.optimizers.Adam(learning_rate=0.0009,amsgrad = 'false') # Defaults to 0.001.
        self.model.compile(optimizer = opt, loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.load_weights(PATH)


    def predict(self, signal : ndarray) -> ndarray:
        y_predicted = self.model.predict(signal.reshape((1,2000)))
        return y_predicted

    def predict_classes(self, signal : ndarray) -> ndarray:
        y_predicted = self.model.predict(signal.reshape((1,2000)))
        y_predicted = y_predicted.argmax(axis=1)
        return y_predicted