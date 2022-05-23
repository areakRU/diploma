import numpy as np

class Cutter:
    def __init__(self, signal, CUT_SIZE, THRESHOLD, THRESHOLD_MAX):
        ''' 
            signal.shape должен быть равен (n,) \n
            CUT_SIZE - длина разрезанного сигнала \n
            THRESHOLD - значение, используемое для нахождения движений в сигнале \n
            THRESHOLD_MAX - значение, используемое для отсечения "выбросов" в сигнале.
        '''
        self.signal = signal
        self.CUT_SIZE = CUT_SIZE #2000
        self.THRESHOLD = THRESHOLD #15000
        self.THRESHOLD_MAX = THRESHOLD_MAX # 350000
        self.cut_signals = np.empty(shape=(1,CUT_SIZE))


    def cut_signal(self) -> np.ndarray:
        '''
            Может получиться так, что метод вернет пустой массив, поэтому необходимо проверять значения массива.
        '''
        mean_signal_value = self.signal.mean()
        threshold_value = mean_signal_value + self.THRESHOLD
        for i in range(self.signal.shape[0] - self.CUT_SIZE):
            max_slider_value = self.signal[i:i+self.CUT_SIZE].max()
            if abs(max_slider_value) < self.THRESHOLD_MAX:
                id_max_slider_value = self.signal[i:i+self.CUT_SIZE].argmax()
                if max_slider_value > threshold_value and id_max_slider_value == np.rint(self.CUT_SIZE/2):
                    cut_signal = self.signal[i:i+self.CUT_SIZE].reshape((1,self.CUT_SIZE))
                    self.cut_signals = np.append(self.cut_signals, cut_signal, axis=0)
        self.cut_signals = np.delete(self.cut_signals, 0, axis=0)
        return self.cut_signals