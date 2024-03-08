import numpy as np
from scipy.ndimage import convolve
from vital.pipeline_package.base import SignalProcessingStep


class Smooth(SignalProcessingStep):
    def __init__(self, window_size=5, **kwargs):
        super().__init__(**kwargs)
        self.window_size = window_size
        self.kernel = np.ones(window_size) / window_size
        self.smoothed_signals = None

    def apply(self, rgb):
        self.smoothed_signals = np.zeros_like(rgb)
        for channel in range(3):
            self.smoothed_signals[:, channel] = convolve(rgb[:, channel], self.kernel, mode='reflect')
        return self.smoothed_signals

    def description(self):
        return f"{self.__class__.__name__}(window_size={self.window_size})"
