from .utils import *
from .visualizer import *
import numpy as np
import scipy


class VitalCalculator:
    def __init__(self, ppg, fs):
        self.ppg = ppg
        self.fs = fs
        self.peaks = None
        self.ibis = None

        self.fft_hr = 0
        self.ibi_hr = 0
        self.hrv = 0


    def calc_fft_hr(self):
        signal = np.expand_dims(self.ppg, 0)
        N = next_power_of_2(signal.shape[1])
        f_ppg, pxx_ppg = scipy.signal.periodogram(signal, fs=self.fs, nfft=N, detrend=False)
        pxx_ppg = pxx_ppg.squeeze()

        # get hr range
        f_ppg = f_ppg.squeeze()
        fmask_ppg = np.argwhere((f_ppg >= 0.75) & (f_ppg <= 2.5))

        masked_ppg = np.take(f_ppg, fmask_ppg)
        masked_pxx_ppg = np.take(pxx_ppg, fmask_ppg).squeeze()

        masked_fft_hr_ppg = np.take(masked_ppg, np.argmax(masked_pxx_ppg)) * 60
        self.fft_hr = masked_fft_hr_ppg

        return masked_fft_hr_ppg

    def calc_ibi_hr(self):
        self.peaks, self.ibis = peak_detection(self.ppg, self.fs, 45, 150, windowsize=60 / self.fft_hr if self.fft_hr > 45 else 0.75)
        self.peaks = [peak for peak in self.peaks if self.ppg[peak] > 0.8]
        hr_list = np.divide(60000, self.ibis)
        self.ibi_hr = np.mean(hr_list)
        return self.ibi_hr

    def calc_hrv(self):
        if self.ibis is None:
            self.calc_ibi_hr()
        self.hrv = np.std(self.ibis, ddof=1)
        return self.hrv
