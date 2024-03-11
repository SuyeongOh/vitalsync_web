import numpy as np
from scipy import sparse
from server.vital.pipeline_package.base import SignalProcessingStep


class Detrend(SignalProcessingStep):
    def __init__(self, lambda_value=100, **kwargs):
        super().__init__(**kwargs)
        self.lambda_value = lambda_value

    def apply(self, input_signal):
        signal_length = input_signal.shape[0]
        # observation matrix
        H = np.identity(signal_length)
        ones = np.ones(signal_length)
        minus_twos = -2 * np.ones(signal_length)
        diags_data = np.array([ones, minus_twos, ones])
        diags_index = np.array([0, 1, 2])
        D = sparse.spdiags(diags_data, diags_index,
                           (signal_length - 2), signal_length).toarray()
        filtered_signal = np.dot(
            (H - np.linalg.inv(H + (self.lambda_value ** 2) * np.dot(D.T, D))), input_signal)
        return filtered_signal

    def description(self):
        return f"{self.__class__.__name__}(lambda={self.lambda_value})"
