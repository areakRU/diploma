import os
from sysconfig import get_path
import numpy as np
from Cutter import Cutter
from Filter import Filter
import pandas as pd

class GetDataFromFiles:
    def __init__(self):
        self.DATA_PATH, self.SAVE_PATH = self.get_paths()
        self.df_data = None
        self.signals = None
        self.labels = None


    def get_paths(self):
        DATA_PATH = os.path.split(os.path.abspath(__file__))[0]
        DATA_PATH = "\\".join(DATA_PATH.split('\\')[0:-1]) + '\\' + 'Data'
        SAVE_PATH = os.path.split(os.path.abspath(__file__))[0]
        SAVE_PATH = "\\".join(DATA_PATH.split('\\')[0:-1]) + '\\' + 'PreparedData'

        if not os.path.exists(DATA_PATH):
            os.mkdir(DATA_PATH)
        if not os.path.exists(SAVE_PATH):
            os.mkdir(SAVE_PATH)

        return DATA_PATH, SAVE_PATH


    def construct_numpy_arrays(self):
        self.signals = np.zeros(shape=(1,2000))
        self.labels = np.zeros(shape=(1,1), dtype=int)

        files = os.listdir(self.DATA_PATH)
        for file_name in files:
            signal = np.loadtxt(self.DATA_PATH + '\\' + file_name)
            filter = Filter(signal, 8)
            filt_signal = filter.filtfilt()
            cutter = Cutter(filt_signal, 2000, 8000, 500000)
            cut_filt_signals = cutter.cut_signal()
            for cut_filt_singal in cut_filt_signals:
                if 'left' in file_name:
                    self.labels = np.append(self.labels, np.array([0]).reshape((1,1)), axis = 0)
                if 'right' in file_name:
                    self.labels = np.append(self.labels, np.array([1]).reshape((1,1)), axis = 0)
                if 'up' in file_name:
                    self.labels = np.append(self.labels, np.array([2]).reshape((1,1)), axis = 0)
                if 'down' in file_name:
                    self.labels = np.append(self.labels, np.array([3]).reshape((1,1)), axis = 0)
                if 'click' in file_name:
                    self.labels = np.append(self.labels, np.array([4]).reshape((1,1)), axis = 0)
                if 'fist' in file_name:
                    self.labels = np.append(self.labels, np.array([5]).reshape((1,1)), axis = 0)
                self.signals = np.append(self.signals, cut_filt_singal.reshape(1,2000), axis = 0)
        self.signals = np.delete(self.signals, 0, axis = 0)
        self.labels = np.delete(self.labels, 0, axis = 0)
        

    def get_pandas(self) -> pd.DataFrame:
        self.construct_numpy_arrayss()
        self.df_data = None

        flag = 0
        for i in range(self.signals.shape[0]):
            data = {'movement_type': self.labels[i][0], 'signal': [list(self.signals[i])]}
            df_data_temp = pd.DataFrame(data)
            if flag == 0:
                self.df_data = pd.DataFrame(data)
                flag = 1
                continue
            self.df_data = pd.concat([self.df_data, df_data_temp], ignore_index=True)
        self.df_data.reset_index(drop=True, inplace=True)

        return self.df_data


    def get_singals(self) -> np.ndarray:
        ''' Returns numpy array of signals '''

        return self.signals


    def get_labels(self) -> np.ndarray:
        ''' Returns numpy array of labels '''

        return self.labels


    def save_numpy_array(self):
        ''' 
            Creates two files:
            1: np_signals.txt - contains cut signals
            2: np_labels.txt - contains label for each cut signal
         '''

        np.savetxt(self.SAVE_PATH + '\\np_signals.txt', self.signals)
        np.savetxt(self.SAVE_PATH + '\\np_lables.txt', self.labels)


    def save_pandas(self):
        '''
            Creates file df_data.csv
        '''
        self.df_data.to_csv(self.SAVE_PATH + '\\df_data.csv', index = False)


    def show_count_of_gestures(self):
        files = os.listdir(self.DATA_PATH)
        left = 0
        right = 0
        up = 0
        down = 0
        click = 0
        fist = 0
        for file_name in files:
            if 'left' in file_name:
                left = left + 1
            if 'right' in file_name:
                right = right + 1
            if 'up' in file_name:
                up = up + 1
            if 'down' in file_name:
                down = down + 1
            if 'click' in file_name:
                click = click + 1
            if 'fist' in file_name:
                fist = fist + 1
        print('left: ' + str(left))
        print('right: ' + str(right))
        print('up: ' + str(up))
        print('down: ' + str(down))
        print('click: ' + str(click))
        print('fist: ' + str(fist))

data = GetDataFromFiles()
# data.show_count_of_gestures()
data.construct_numpy_arrays()
data.save_numpy_array()