from matplotlib import pyplot as plt
import os
import scipy
import numpy as np


class SignalProcessingStep:
    def __init__(self, **kwargs):
        self.params = kwargs

    def apply(self, sig):
        raise NotImplementedError("Each processing step must implement the 'apply' method.")

    def visualize(self, ppg, save_dict):
        fs = 30
        """Plot the given signal and FFT of the signal."""
        fig, axs = plt.subplots(3, 1, figsize=save_dict['figsize'])
        plt.rc('font', size=save_dict['fontsize'])
        plt.rc('axes', titlesize=save_dict['fontsize'])
        plt.rc('axes', labelsize=save_dict['fontsize'])
        plt.rc('xtick', labelsize=save_dict['fontsize'])
        plt.rc('ytick', labelsize=save_dict['fontsize'])
        plt.rc('legend', fontsize=save_dict['fontsize'])
        plt.rc('figure', titlesize=save_dict['fontsize'])
        ####################################################################################################################
        name = save_dict['name']
        desc = save_dict['desc']
        save_root_path = save_dict['save_root_path']
        seq_num = save_dict['seq_num']
        model_name = save_dict['model']
        if not isinstance(ppg, list):
            ppg = [ppg]
        ####################################################################################################################
        for signal in ppg:
            # Plot signal @Time Domain with peak dots
            # peaks_pred, _ = find_peaks(signal, distance=save_dict["peak_distance"])
            axs[0].plot(signal, label=model_name, color='blue')
            axs[0].set_title(f"{name} | {model_name} : {desc} @Time Domain")
            axs[0].legend(loc='upper right')
            axs[0].grid()
            ################################################################################################################
            # Calculate FFT of predictions
            signal = np.expand_dims(signal, 0)
            N = self.next_power_of_2(signal.shape[1])
            f_pred, pxx_pred = scipy.signal.periodogram(signal, fs=fs, nfft=N, detrend=False)
            pxx_pred = pxx_pred.squeeze()

            # Crop pred freq signal under 6Hz
            fmask_pred = np.argwhere(f_pred < 6)
            f_pred = np.take(f_pred, fmask_pred)
            pxx_pred = np.take(pxx_pred, fmask_pred).squeeze()

            # Find pred freq signal peak
            fft_hr_pred = np.take(f_pred, np.argmax(pxx_pred)) * 60

            # Plot peak of pred signal using fft_hr_pred
            # peaks_pred, _ = self.peak_detection(ppg=signal.squeeze(), fs=fs, bpmmin=45, bpmmax=150,
            #                                windowsize=60 / fft_hr_pred if fft_hr_pred > 0 else 0.75)
            # axs[0].plot(peaks_pred, signal.squeeze()[peaks_pred], "o", color='orange')

            # Plot FFT of prediction and label
            axs[1].plot(f_pred * 60, pxx_pred, label=model_name, color='blue')
            axs[1].plot(fft_hr_pred, np.max(pxx_pred), 'bo')

            # Plot vertical line of peak
            axs[1].axvline(x=fft_hr_pred, color='b', linestyle='--')
            peak_y = axs[1].get_ylim()[1] if np.max(pxx_pred) > axs[1].get_ylim()[1] else np.max(pxx_pred)
            axs[1].text(fft_hr_pred, peak_y, str(np.round(fft_hr_pred, 2)) + ' BPM',
                        horizontalalignment='right', color='blue', bbox=dict(facecolor='white', alpha=0.7))
            ################################################################################################################
            # Plot vertical line of 45~150 BPM
            lower_bound = 45
            upper_bound = 150
            axs[1].axvline(x=lower_bound, color='red', linewidth=2)
            axs[1].axvline(x=upper_bound, color='red', linewidth=2)
            axs[1].axvspan(45, 150, color='yellow', alpha=0.3)

            # Set options
            axs[1].set_title(f"{name} | {model_name} : {desc} @Frequency Domain")
            axs[1].legend(loc='upper right')
            axs[1].grid()
            ################################################################################################################
            # Find peak of pred freq signal in 45~150 BPM
            f_pred = f_pred.squeeze()
            fmask_pred = np.argwhere((f_pred >= 0.75) & (f_pred <= 2.5))
            masked_pred = np.take(f_pred, fmask_pred)
            masked_pxx_pred = np.take(pxx_pred, fmask_pred).squeeze()
            masked_fft_hr_pred = np.take(masked_pred, np.argmax(masked_pxx_pred)) * 60

            # Plot FFT of prediction
            axs[2].plot(masked_pred * 60, masked_pxx_pred, label=model_name, color='blue')
            axs[2].plot(masked_fft_hr_pred, np.max(masked_pxx_pred), 'bo')

            # Plot vertical line of peak
            axs[2].axvline(x=masked_fft_hr_pred, color='b', linestyle='--')
            peak_y = axs[2].get_ylim()[1] if np.max(masked_pxx_pred) > axs[2].get_ylim()[1] else np.max(masked_pxx_pred)
            axs[2].text(masked_fft_hr_pred, peak_y, str(np.round(masked_fft_hr_pred, 2)) + ' BPM',
                        horizontalalignment='right', color='blue', bbox=dict(facecolor='white', alpha=0.7))
            ################################################################################################################
            # Plot vertical line of 45~150 BPM
            lower_bound = 45
            upper_bound = 150
            axs[2].axvline(x=lower_bound, color='red', linewidth=2)
            axs[2].axvline(x=upper_bound, color='red', linewidth=2)
            axs[2].axvspan(45, 150, color='yellow', alpha=0.3)
            ################################################################################################################
            # Set options
            axs[2].set_title(f"{name} | {model_name} : {desc} @HR Range")
            axs[2].legend(loc='upper right')
            axs[2].grid()
            plt.tight_layout()
            ################################################################################################################
            # Save plot
            save_path = f"{save_root_path}/{model_name}_{name}".replace(' ', '_')
            if not os.path.isdir(save_path):
                os.makedirs(save_path)
            plt.savefig(f"{save_path}/{seq_num}_{name}_{model_name}_{desc}_bvp_fft.png".replace(' ', '_'), dpi=300)
            if save_dict['show_flag']:
                plt.show()
            plt.close()

    def description(self):
        return f"{self.__class__.__name__}()"

    def next_power_of_2(self, x):
        """Calculate the nearest power of 2."""
        return 1 if x == 0 else 2 ** (x - 1).bit_length()
