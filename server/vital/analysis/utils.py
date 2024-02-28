from heartpy.datautils import rolling_mean
from heartpy.peakdetection import fit_peaks
import numpy as np


def next_power_of_2(x):
    """Calculate the nearest power of 2."""
    return 1 if x == 0 else 2 ** (x - 1).bit_length()


def peak_detection(ppg, fs, bpmmin=45, bpmmax=150, windowsize=0.75):
    rol_mean = rolling_mean(ppg, windowsize, fs)
    wd = fit_peaks(ppg, rol_mean, fs, bpmmin, bpmmax)

    return wd['peaklist'], wd['RR_list']

