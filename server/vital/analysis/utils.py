import numpy as np
import torch
from heartpy.datautils import rolling_mean
from heartpy.peakdetection import fit_peaks, calc_rr, check_peaks
from scipy.signal import butter, filtfilt, lfilter, hilbert, find_peaks

from server.vital.analysis.core.bp.models import patcherx


def next_power_of_2(x):
    """Calculate the nearest power of 2."""
    return 1 if x == 0 else 2 ** (x - 1).bit_length()


def peak_detection(ppg, fs, bpmmin=45, bpmmax=150, windowsize=0.75):
    rol_mean = rolling_mean(ppg, windowsize, fs)
    wd = fit_peaks(ppg, rol_mean, fs, bpmmin, bpmmax)
    wd = calc_rr(wd['peaklist'], fs, working_data=wd)
    wd = check_peaks(wd['RR_list'], wd['peaklist'], wd['ybeat'], reject_segmentwise=True, working_data=wd)
    peaklist_cor = np.array(wd['peaklist'])[np.where(wd['binary_peaklist'])[0]]

    return peaklist_cor, wd['RR_list_cor']


def BPF(input_val, fs=30, low=0.75, high=2.5):
    low = low / (0.5 * fs)
    high = high / (0.5 * fs)
    [b_pulse, a_pulse] = butter(6, [low, high], btype='bandpass')
    return filtfilt(b_pulse, a_pulse, np.double(input_val))

    wd = calc_rr(wd['peaklist'], fs, working_data=wd)
    wd = check_peaks(wd['RR_list'], wd['peaklist'], wd['ybeat'], reject_segmentwise=True, working_data=wd)
    peaklist_cor = np.array(wd['peaklist'])[np.where(wd['binary_peaklist'])[0]]

def BPF_new(input_val, fs=30, low=0.75, high=2.5,order = 6):
    low = low / (0.5 * fs)
    high = high / (0.5 * fs)
    [b_pulse, a_pulse] = butter(order, [low, high], btype='bandpass')
    if isinstance(input_val, torch.Tensor):
        input_val = input_val.cpu().numpy()

    input_val = np.double(input_val)

    # Save original mean and standard deviation
    original_mean = np.mean(input_val)
    original_std = np.std(input_val)

    # Apply bandpass filter
    filtered_val = filtfilt(b_pulse, a_pulse, input_val)

    # Restore the original mean and standard deviation
    filtered_val = (filtered_val - np.mean(filtered_val)) * (original_std / np.std(filtered_val)) + original_mean

    return filtered_val

def butter_lowpass_filter(data, fs, cutoff=0.7, order=1):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y


def calculate_envelopes(signal):
    """
    Calculate the upper and lower envelopes of a signal using Hilbert Transform.
    """
    analytic_signal = hilbert(signal)
    upper_envelope = np.abs(analytic_signal)
    lower_envelope = -np.abs(analytic_signal)
    return upper_envelope, lower_envelope


def calculate_peak_valley_distance(upper_envelope, lower_envelope):
    """
    Calculate the peak-valley distance from the upper and lower envelopes of the signal.
    """
    peak_valley_distance = np.median(upper_envelope - lower_envelope)
    return peak_valley_distance


def find_filtered_peaks(signal, dist=15):
    p, _ = find_peaks(signal, distance=dist)
    v, _ = find_peaks(-signal, distance=dist)

    # valley가 앞에 있으면 valley peak 앞에서 하나씩 삭제
    # peak가 앞에 있으면 peak 하나 삭제

    peaks, valleys = filter_peaks_and_valleys(peaks=p, valleys=v, signal=signal)

    if peaks[0] < valleys[0]:
        peaks = peaks[2:]
        valleys = valleys[1:]
    else:
        peaks = peaks[1:]
        valleys = valleys[1:]

    num_pair = min(len(peaks), len(valleys))
    if len(valleys) > num_pair:
        valleys = valleys[:num_pair]

    return peaks, valleys


def filter_peaks_and_valleys(peaks, valleys, signal):
    filtered_peaks = []
    filtered_valleys = []

    # 모든 peaks와 valleys를 하나의 배열로 합치고, 정렬합니다.
    all_points = np.sort(np.concatenate((peaks, valleys)))

    # 첫 번째 peak 또는 valley부터 시작하여, 다음 peak 또는 valley 사이에서 조건을 확인합니다.
    for i in range(len(all_points) - 1):
        current_point = all_points[i]
        next_point = all_points[i + 1]

        # 현재 점이 peak일 경우
        if current_point in peaks:
            # 다음 점이 valley이고, 사이에 다른 점이 없으면, 현재 peak를 유지합니다.
            if next_point in valleys and i + 2 < len(all_points) and all_points[i + 2] not in valleys:
                filtered_peaks.append(current_point)
            # 사이에 다른 peaks가 있는 경우, 최댓값을 찾아 필터링합니다.
            elif next_point in valleys:
                max_peak = signal[current_point]
                max_peak_index = current_point
                for j in range(current_point + 1, next_point):
                    if j in peaks and signal[j] > max_peak:
                        max_peak = signal[j]
                        max_peak_index = j
                filtered_peaks.append(max_peak_index)
        # 현재 점이 valley일 경우
        else:
            # 다음 점이 peak이고, 사이에 다른 점이 없으면, 현재 valley를 유지합니다.
            if next_point in peaks and i + 2 < len(all_points) and all_points[i + 2] not in peaks:
                filtered_valleys.append(current_point)
            # 사이에 다른 valleys가 있는 경우, 최솟값을 찾아 필터링합니다.
            elif next_point in peaks:
                min_valley = signal[current_point]
                min_valley_index = current_point
                for j in range(current_point + 1, next_point):
                    if j in valleys and signal[j] < min_valley:
                        min_valley = signal[j]
                        min_valley_index = j
                filtered_valleys.append(min_valley_index)

    return np.array(filtered_peaks), np.array(filtered_valleys)

def closest_pairs(a, b):
    used_a = set()
    used_b = set()
    result_a = []
    result_b = []

    for _ in range(min(len(a), len(b))):
        min_diff = float('inf')
        pair = (None, None)

        for i in range(len(a)):
            if i in used_a:
                continue
            for j in range(len(b)):
                if j in used_b:
                    continue
                diff = abs(a[i] - b[j])
                if diff < min_diff:
                    min_diff = diff
                    pair = (i, j)

        if pair != (None, None):
            used_a.add(pair[0])
            used_b.add(pair[1])
            result_a.append(a[pair[0]])
            result_b.append(b[pair[1]])

    return np.array(result_a), np.array(result_b)


def load_bp_model():
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        bp_model = patcherx.Model().to(device).float()
        bp_model.load_state_dict(torch.load('core/bp/pretrained_weights/patcherx_best.pth', map_location=torch.device("cpu")))
        bp_model.eval()
        print("Model loaded successfully.")
    except FileNotFoundError:
        print("Model file not found. Please check the file path and try again.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return bp_model
