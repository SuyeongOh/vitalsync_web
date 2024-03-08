from vital.pipeline_package.base import SignalProcessingStep
from scipy.signal import butter, filtfilt
import numpy as np


class BandpassFilter(SignalProcessingStep):
    def __init__(self, low, high, fs, order=2, filter_type="butterworth", **kwargs):
        super().__init__(**kwargs)
        self.low = low
        self.high = high
        self.fs = fs
        self.filter_type = filter_type
        self.order = order

    def apply(self, signal):
        if self.filter_type == "butterworth":
            return self._butterworth_filter(signal)
        else:
            raise ValueError(f"Filter type '{self.filter_type}' is not supported.")

    def _butterworth_filter(self, signal):
        [b, a] = butter(N=self.order, Wn=[self.low / self.fs * 2, self.high / self.fs * 2], btype='bandpass')
        filtered_signal = filtfilt(b, a, signal.astype(np.double))
        return filtered_signal

    def description(self):
        # 매개변수 정보를 포함하는 description 구현
        return f"{self.__class__.__name__}(low={self.low}, high={self.high}, fs={self.fs}, filter_type='{self.filter_type}')"
