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
        classes = 5

        self.model = Sequential()
        self.model.add(InputLayer(input_shape=(2000,)))
        self.model.add(Reshape((2000,1), input_shape=(2000,)))
        self.model.add(BatchNormalization())
        self.model.add(Conv1D(100,50,activation='relu', strides=2))
        self.model.add(Conv1D(75,50,activation='relu'))
        self.model.add(Dropout(0.1))
        self.model.add(Conv1D(75,50,activation='relu', strides=2))
        self.model.add(Conv1D(75,40,activation='relu'))
        self.model.add(BatchNormalization())
        self.model.add(MaxPooling1D(2))
        self.model.add(Conv1D(75,40,activation='relu'))
        self.model.add(Conv1D(100,30,activation='relu'))
        self.model.add(Conv1D(150,30,activation='relu'))
        self.model.add(BatchNormalization())
        self.model.add(MaxPooling1D())
        self.model.add(Dropout(0.3))
        self.model.add(Flatten())
        self.model.add(Dense(classes, activation='softmax'))

        opt = adam_v2.Adam()
        self.model.compile(optimizer = opt, loss='categorical_crossentropy', metrics=['accuracy'])
        self.model.load_weights(PATH)
        self.model.summary()


    def predict(self, signal : ndarray) -> ndarray:
        y_predicted = self.model.predict(signal.reshape((1,2000)))
        return y_predicted

    def predict_classes(self, signal : ndarray) -> ndarray:
        y_predicted = self.model.predict(signal.reshape((1,2000)))
        y_predicted = np.round(y_predicted).argmax(axis=1)
        return y_predicted