from server.vital.pipeline_package.base import SignalProcessingStep
import numpy as np
from scipy.signal import hilbert


class HilbertNormalization(SignalProcessingStep):
    def __init__(self):
        super().__init__()

    def apply(self, signal):
        analytic_signal = hilbert(signal)
        amplitude_envelope = np.abs(analytic_signal)
        normalized_signal = signal / amplitude_envelope
        return normalized_signal

    def description(self):
        return f"{self.__class__.__name__}()"
