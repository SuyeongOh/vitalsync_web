from heartpy.datautils import rolling_mean
from heartpy.peakdetection import fit_peaks, calc_rr, check_peaks
import numpy as np
import torch
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

def load_bp_model(bp_model):
    if bp_model is None:
        try:
            bp_model = patcherx.Model()
            bp_model.load_state_dict(torch.load('./pretrained_weights/patcherx_best.pth'))
            bp_model.eval()
            print("Model loaded successfully.")
        except FileNotFoundError:
            print("Model file not found. Please check the file path and try again.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    return bp_model
