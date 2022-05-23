from numpy import ndarray
from scipy.ndimage import uniform_filter1d

class Filter:
    def filtfilt(self) -> ndarray:
        filtered_data = uniform_filter1d(self.data, size=self.filter_size, mode='nearest')
        return filtered_data


    def __init__(self, data, filter_size):
        self.data = data
        self.filter_size = filter_size