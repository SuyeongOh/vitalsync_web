from server.vital.analysis.core.bp import trainer
from server.vital.analysis.visualizer import *
import numpy as np
import scipy
from server.vital.pipeline_package import *


class VitalCalculator:
    def __init__(self, ppg, fs, save_dict):
        self.ppg = detrend.Detrend().apply(ppg)
        self.fs = fs
        self.model = save_dict['model']
        self.save_dict = save_dict
        self.visualize_ppg()


        # HR related
        self.ppg_hr = heartrate_pipeline.apply(self.ppg, save_dict)
        self.peaks = None
        self.ibis = None
        self.fft_hr = 0
        self.ibi_hr = 0
        self.hrv = 0
        self.hrv_confidence = 0

        # LF/HF related
        self.save_dict['show_flag'] = False
        self.ppg_lf_hf = lf_hf_pipeline.apply(self.ppg, self.save_dict)
        self.lf_hf_ratio = 0
        # LF/HF related
        self.ppg_lf_hf = lf_hf_pipeline.apply(self.ppg, self.save_dict)
        self.lf_hf_ratio = 0

        # SpO2 related
        self.spo2 = 0

        # bp_model definition
        self.bp_model = None

    def visualize_ppg(self):
        bvp_fft_plot(self.ppg, self.fs, self.save_dict)
    #
    # def visualize_rgb(self, rgb):
    #     rgb_plot(rgb, self.save_dict)

    def calc_fft_hr(self):
        hilbert_ppg = HilbertNormalization().apply(self.ppg_hr)
        signal = np.expand_dims(hilbert_ppg, 0)
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
        self.peaks, self.ibis = peak_detection(self.ppg_hr, self.fs, 45, 150,
                                               windowsize=60 / self.fft_hr if self.fft_hr > 0 else 0.75)
        # self.ibis = np.diff(self.peaks) / self.fs * 1000
        hr_list = np.divide(60000, self.ibis)
        self.ibi_hr = np.mean(hr_list)
        return self.ibi_hr

    def calc_hrv(self):
        self.hrv = np.std(self.ibis)
        return self.hrv

    def calc_hrv_confidence(self):
        self.hrv_confidence = np.exp(-abs(self.fft_hr - self.ibi_hr) / 20)  # 95% : 1.02, 90% : 2.11
        return self.hrv_confidence

    def calc_baevsky_stress_index(self):
        smallest = np.min(self.ibis)
        highest = np.max(self.ibis)
        hist, bin_edges = np.histogram(self.ibis, bins=np.arange(smallest, highest, 50))

        mode_index = np.argmax(hist)
        mode_bin = bin_edges[mode_index]
        mode_frequency = hist[mode_index]
        total_rr_intervals = len(self.ibis)

        amo = (mode_frequency / total_rr_intervals) * 100

        self.b_si = np.sqrt(amo / (2 * mode_bin) * (highest - smallest))
        return self.b_si

    def calc_lfhf(self):
        low_frequency = (0.04, 0.15)
        high_frequency = (0.15, 0.4)

        expanded_signal = np.expand_dims(self.ppg_lf_hf, 0)
        N = next_power_of_2(expanded_signal.shape[1])
        f, pxx = scipy.signal.periodogram(self.ppg_lf_hf, self.fs, nfft=N, detrend=False)

        # Find the low frequency and high frequency indices
        lf_indices = np.where((f >= low_frequency[0]) & (f <= low_frequency[1]))
        hf_indices = np.where((f >= high_frequency[0]) & (f <= high_frequency[1]))

        # Calculate the LF and HF power
        lf_power = np.trapz(pxx[lf_indices], f[lf_indices])
        hf_power = np.trapz(pxx[hf_indices], f[hf_indices])

        # Calculate the LF/HF ratio
        self.lf_hf_ratio = lf_power / hf_power
        return self.lf_hf_ratio

    def calc_spo2(self, RGB):
        r_sig = bandpassfilter.BandpassFilter(filter_type="butterworth", fs=30, low=0.75, high=2.5, order=6).apply(RGB[:, 0])
        b_sig = bandpassfilter.BandpassFilter(filter_type="butterworth", fs=30, low=0.75, high=2.5, order=6).apply(RGB[:, 2])

        r_mean = np.mean(r_sig)
        r_std = np.std(r_sig)

        b_mean = np.mean(b_sig)
        b_std = np.std(b_sig)

        R = (r_std / r_mean) / (b_std / b_mean)

        self.spo2 = 97.61 + 0.42 * R
        return self.spo2

    def calc_bp(self, rgb, hr, age, gender):
        if self.bp_model is None:
            self.bp_model = load_bp_model(self.bp_model)

        mbp = self.bp_model.forward(rgb, hr, age, gender)

        print(f'mbp :: {mbp}')

        return mbp