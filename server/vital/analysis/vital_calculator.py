import numpy as np
import scipy.signal.windows
import torch
from scipy.signal.windows import hamming

from server.vital.analysis.core.bp.datasets import vitalvideos5input_dataset
from server.vital.analysis.core.ppg import pos
from server.vital.analysis.visualizer import *
from server.vital.pipeline_package import *


class VitalCalculator:
    def __init__(self, ppg, fs):
        self.ppg = detrend.Detrend().apply(ppg)
        self.fs = fs
        self.save_dict = None
        # self.model = save_dict['model']
        # self.save_dict = save_dict


        # HR related
        self.bpf_ppg = heartrate_pipeline.apply(self.ppg)
        self.hilbert_ppg = fft_hr_pipeline.apply(self.bpf_ppg)
        self.peaks = None
        self.ibis = None
        self.fft_hr = 0
        self.ibi_hr = 0
        self.hrv = 0
        self.hrv_confidence = 0

        # LF/HF related
        self.ppg_lf_hf = lf_hf_pipeline.apply(self.ppg)
        self.lf_hf_ratio = 0

        # SpO2 related
        self.spo2 = 0

        # BP related
        self.sbp = 0
        self.dbp = 0

        # BR related
        self.ppg_breathrate = breathrate_pipeline.apply(self.ppg)
        self.br = 0
        # bp_model definition
        self.bp_model = load_bp_model()

    def visualize_ppg(self):
        bvp_fft_plot(self.ppg, self.fs, self.save_dict)
    #
    # def visualize_rgb(self, rgb):
    #     rgb_plot(rgb, self.save_dict)

    def calc_fft_hr(self):
        signal = np.expand_dims(self.hilbert_ppg, 0)
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
        try:
            self.peaks, self.ibis = peak_detection(self.bpf_ppg, self.fs, 45, 150,
                                                windowsize=60 / self.fft_hr if self.fft_hr > 0 else 0.75)
            hr_list = np.divide(60000, self.ibis)
            self.ibi_hr = np.mean(hr_list)
        except Exception as e:
            print("IBI error : ")
            print(e)
            self.ibi_hr = 0
        return self.ibi_hr

    def calc_hrv(self):
        try:
            if self.ibis is None:
                self.calc_ibi_hr()
            self.hrv = np.std(self.ibis)
        except Exception as e:
            print("hrv error")
            print(e)
            self.hrv = 0

        return self.hrv

    # def calc_hrv_confidence(self):
    #     self.hrv_confidence = np.exp(-abs(self.fft_hr - self.ibi_hr) / 20)  # 95% : 1.02, 90% : 2.11
    #     return self.hrv_confidence

    def calc_hrv_confidence(self):
        self.hrv_confidence = np.exp(-abs(self.fft_hr - self.ibi_hr) / 20)  # 95% : 1.02, 90% : 2.11
        return self.hrv_confidence

    def calc_baevsky_stress_index(self):
        try:
            smallest = np.min(self.ibis)
            highest = np.max(self.ibis)
            hist, bin_edges = np.histogram(self.ibis, bins=np.arange(smallest, highest, 50))

            mode_index = np.argmax(hist)
            mode_bin = bin_edges[mode_index]
            mode_frequency = hist[mode_index]
            total_rr_intervals = len(self.ibis)

            amo = (mode_frequency / total_rr_intervals) * 100

            self.b_si = np.sqrt(amo / (2 * mode_bin) * (highest - smallest))
        except Exception as e:
            print("stress error")
            print(e)
            self.b_si = -1
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

    # def old_calc_spo2(self, RGB):
    #     r_sig = bandpassfilter.BandpassFilter(filter_type="butterworth", fs=30, low=0.75, high=2.5, order=6).apply(RGB[:, 0])
    #     b_sig = bandpassfilter.BandpassFilter(filter_type="butterworth", fs=30, low=0.75, high=2.5, order=6).apply(RGB[:, 2])
    #
    #     r_mean = np.mean(r_sig)
    #     r_std = np.std(r_sig)
    #
    #     b_mean = np.mean(b_sig)
    #     b_std = np.std(b_sig)
    #
    #     R = (r_std / r_mean) / (b_std / b_mean)
    #
    #     self.spo2 = 97.61 + 0.42 * R
    #     return self.spo2


    def calc_spo2(self, RGB):
        #RoR 계산과정
        if not isinstance(RGB, np.ndarray):
            RGB = np.array(RGB)
        HbO2 = (0.13214285714285712 * RGB[0]) + (0.11964285714285716 * RGB[1]) + (-0.251785714 * RGB[2])
        Hb = (-0.019642857 * RGB[0]) + (- 0.0125 * RGB[1]) + (0.032142857 * RGB[2])
        scale = 10000

        if np.corrcoef(HbO2, Hb)[1][0] < 0:
            Hb *= -1

        HbO2 = BPF_new(HbO2, self.fs, 0.7, 3.0)
        Hb = BPF_new(Hb, self.fs, 0.7, 3.0)

        HbO2 = Detrend().apply_new(HbO2)
        Hb = Detrend().apply_new(Hb)

        HbO2 = (HbO2 - np.mean(HbO2)) * scale
        Hb = (Hb - np.mean(Hb)) * scale



        HbO2_peak, HbO2_valley = find_filtered_peaks(HbO2)
        Hb_peak, Hb_valley = find_filtered_peaks(Hb)

        common_p = np.intersect1d(HbO2_peak, Hb_peak)
        common_v = np.intersect1d(HbO2_valley, Hb_valley)

        filtered_p, filtered_v = closest_pairs(common_p, common_v)

        if len(filtered_p) == 0 or len(filtered_v) == 0:
            return 0

        baseline_correction = np.abs(min(np.min(HbO2), np.min(Hb))) + 1
        hbo2_p = HbO2[filtered_p] + baseline_correction
        hbo2_v = HbO2[filtered_v] + baseline_correction
        ls_hb = np.log(hbo2_v / hbo2_p)
        hb_p = Hb[filtered_p] + baseline_correction
        hb_v = Hb[filtered_v] + baseline_correction

        ls_hbo2 = np.log(hb_v / hb_p)  # hbo2_p - hbo2_v  # np.log(hbo2_p / hbo2_v)
        # ls_hb = hb_p - hb_v
        # ls_hb = np.log(hb_p / hb_v)
        if np.median(ls_hbo2 / ls_hb) > 1:
            RoR = np.median(ls_hbo2 / ls_hb)
        else:
            RoR = np.median(ls_hb / ls_hbo2)

        #SpO2 계산과정
        return -0.783626023 * RoR + 102.42805451382233

    def calc_spo2_lagacy(self, RGB):
        r = RGB[:, 0]
        g = RGB[:, 1]
        window_length = 10 * 30
        stride = 1 * 30
        spo2_list = []
        num_windows = (len(g) - window_length) // stride + 1
        for i in range(num_windows):
            r_dc = butter_lowpass_filter(r[i * stride: i * stride + window_length], 30, 0.7)  # 0.7 Hz 미만 Lowpass
            g_dc = butter_lowpass_filter(g[i * stride: i * stride + window_length], 30, 0.7)  # 0.7 Hz 미만 Lowpass
            r_bpf = BPF(r[i * stride: i * stride + window_length] / r_dc, 30, 0.7, 3.0)
            g_bpf = BPF(g[i * stride: i * stride + window_length] / g_dc, 30, 0.7, 3.0)

            upper_envelope, lower_envelope = calculate_envelopes(r_bpf)
            # 에너벌로프의 중앙값 계산
            r_peak_valley_distance = calculate_peak_valley_distance(upper_envelope, lower_envelope)

            upper_envelope, lower_envelope = calculate_envelopes(g_bpf)
            # 에너벌로프의 중앙값 계산
            g_peak_valley_distance = calculate_peak_valley_distance(upper_envelope, lower_envelope)

            g_p, g_v = find_filtered_peaks(g_bpf)
            r_p, r_v = find_filtered_peaks(r_bpf)

            s_g_p = sum(abs(g_bpf[g_p]))
            s_g_v = sum(abs(g_bpf[g_v]))

            ls_g = np.log(s_g_p / s_g_v)

            s_r_p = sum(abs(r_bpf[r_p]))
            s_r_v = sum(abs(r_bpf[r_v]))

            ls_r = np.log(s_r_p / s_r_v)

            ls_ratio = ls_r / ls_g
            hil_ratio = r_peak_valley_distance / g_peak_valley_distance

            ratio = (ls_ratio + hil_ratio) / 2
            s = -14.80599989961074 * ratio + 112.05782709983683
            spo2_list.append(s)
        self.spo2 = np.mean(spo2_list)
        return self.spo2

    def calc_br(self):


        window_hamming = hamming(len(self.ppg_breathrate))
        signal_hamming = self.ppg_breathrate * window_hamming

        signal = np.expand_dims(signal_hamming, 0)

        N = next_power_of_2(signal.shape[1])
        f_br, pxx_br = scipy.signal.periodogram(signal, fs=self.fs, nfft=N, detrend=False)
        pxx_br = pxx_br.squeeze()

        # get br range
        f_br = f_br.squeeze()
        fmask_br = np.argwhere((f_br >= 0.1) & (f_br <= 1))

        masked_br = np.take(f_br, fmask_br)
        masked_pxx_br = np.take(pxx_br, fmask_br).squeeze()

        masked_fft_br = np.take(masked_br, np.argmax(masked_pxx_br)) * 60

        self.br = masked_fft_br
        return self.br

    def calc_bp(self, height, weight, age, gender):
        Q = 5 if gender == 'male' else 4.5
        # Resistivity of blood
        ROB = 18.31
        # Ejection Time
        ET = (364.5 - 1.23 * self.fft_hr)
        # Body Surface Area
        BSA = 0.007184 * (weight ** 0.425) * (height ** 0.725)
        # Stroke volume
        SV = (-6.6 + (0.25 * (ET - 35)) - (0.62 * self.fft_hr) + (40.4 * BSA) - (0.51 * age))
        # Pulse Pressure
        PP = SV / ((0.013 * weight - 0.007 * age - 0.004 * self.fft_hr) + 1.307)

        MAP = Q * ROB

        self.sbp = int(MAP + 3 / 2 * PP)
        self.dbp = int(MAP - PP / 3)

        return self.sbp, self.dbp


    def calc_mbp(self, rgb, ppg, hr, age, gender):
        if self.bp_model is None:
            self.bp_model = load_bp_model()

        ppg = vitalvideos5input_dataset.min_max_normalize(ppg)
        rgb = np.array(rgb)
        ppg = np.array(ppg)
        hr = np.array(hr)
        age = np.array(age)
        if gender == 'male':
            gender = 0
        elif gender == 'female':
            gender = 1
        gender = np.array(gender)

        mbp = self.bp_model(torch.hstack([torch.tensor(rgb, dtype=torch.float32), torch.tensor(ppg, dtype=torch.float32).unsqueeze(1)]).unsqueeze(0),
                                    torch.tensor(hr, dtype=torch.float32).unsqueeze(0),
                                    torch.tensor(age, dtype=torch.float32).unsqueeze(0),
                                    torch.tensor(gender, dtype=torch.float32).unsqueeze(0))
        print(f'mbp :: {mbp}')

        return mbp

import json

def parse_rgb():
    # 1. 텍스트 파일 읽기
    file_path = 'core/bp/sample_data_ppg.txt'
    with open(file_path, 'r') as file:
        data = file.read()

    # 2. JSON 데이터 파싱
    data_json = json.loads(data)

    # 3. RGB 값 추출
    rgb_values = data_json['RGB']

    # 결과 확인
    print(rgb_values)
    return np.array(rgb_values)

if __name__ == '__main__':
    #pred_ppg = np.random.uniform(-1,1, size=600).astype(np.float32)
    rgb = parse_rgb()
    # Calculate PPG
    RGB = np.asarray(rgb).transpose(1, 0)
    #RGB = preprocess_pipeline.apply(RGB)

    # Calculate PPG
    pred_ppg = pos.POS(RGB, 30)
    #pred_ppg = vitalvideos5input_dataset.min_max_normalize(pred_ppg)

    vitalcalc = VitalCalculator(pred_ppg, 30)
    # mbp = vitalcalc.calc_mbp(RGB, pred_ppg, 80, 25, "male")
    spo2 = vitalcalc.calc_spo2(rgb)
    print(spo2)
