import numpy as np
from scipy import sparse
from scipy.sparse import spdiags

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

    def apply_new(self, signal, Lambda = 100):

        """detrend(signal, Lambda) -> filtered_signal
        This function applies a detrending filter.
        This  is based on the following article "An advanced detrending method with application
        to HRV analysis". Tarvainen et al., IEEE Trans on Biomedical Engineering, 2002.
        *Parameters*
          ``signal`` (1d numpy array):
            The signal where you want to remove the trend.
          ``Lambda`` (int):
            The smoothing parameter.
        *Returns*
          ``filtered_signal`` (1d numpy array):
            The detrended signal.
        """
        signal_length = len(signal)

        # observation matrix
        H = np.identity(signal_length)

        # Second-order difference matrix
        ones = np.ones(signal_length)
        minus_twos = -2 * np.ones(signal_length)
        diags_data = np.array([ones, minus_twos, ones])
        diags_index = np.array([0, 1, 2])
        D = spdiags(diags_data, diags_index, (signal_length - 2), signal_length).toarray()

        # Filter the signal
        filtered_signal = np.dot((H - np.linalg.inv(H + (Lambda ** 2) * np.dot(D.T, D))), signal)

        # Preserve the original scale
        min_signal = np.min(signal)
        max_signal = np.max(signal)
        min_filtered = np.min(filtered_signal)
        max_filtered = np.max(filtered_signal)

        # Rescale the filtered signal to the original signal range
        filtered_signal_rescaled = (filtered_signal - min_filtered) / (max_filtered - min_filtered) * (
                max_signal - min_signal) + min_signal
        return filtered_signal_rescaled

    def description(self):
        return f"{self.__class__.__name__}(lambda={self.lambda_value})"
