import cv2
import os
import json
from collections import defaultdict
import glob
import face_recognition
from server.vital.analysis.core.ppg import pos
from server.vital.pipeline_package import *
from server.vital.analysis.utils import *
from server.vital.analysis.core.bp import config
import scipy
from tqdm import tqdm
import h5py


def get_raw_data(config):
    data_path = config.DATA.DATASET_PATH
    if config.DATA.DATASET in ["vv100", "vv250"]:
        data_dirs = glob.glob(data_path + os.sep + "*.json")
        if not data_dirs:
            raise FileNotFoundError("No data found in the specified path")
        dirs = [{"index": i, "subject": os.path.basename(data_dir).split(".")[0], "path": data_dir} for i, data_dir in
                enumerate(data_dirs)]
        return dirs


def gender_to_onehot(gender):
    if gender == 'F':
        return [1, 0]  # 여성인 경우 [1, 0]으로 인코딩
    elif gender == 'M':
        return [0, 1]  # 남성인 경우 [0, 1]로 인코딩
    else:
        raise ValueError("Invalid gender value")


def read_wave(wave_file, config):
    wave_dict = defaultdict()
    if config.DATA.DATASET in ["vv100", "vv250"]:
        with open(wave_file, 'r') as f:
            json_data = json.load(f)
            subject_id = json_data['GUID']
            wave_dict[subject_id] = defaultdict()
            flag_bp = False
            for scenario in json_data['scenarios']:
                if 'bp_sys' in scenario['recordings']:
                    wave_dict[subject_id]['video'] = scenario['recordings']['RGB']['filename']
                    wave_dict[subject_id]['age'] = int(json_data['participant']['age'])
                    wave_dict[subject_id]['gender'] = gender_to_onehot(json_data['participant']['gender'])
                    # wave_dict[subject_id]['ppg'] = [ppg[:] for ppg in scenario['recordings']['ppg']['timeseries']]
                    # wave_dict[subject_id]['hr'] = [hr[:] for hr in scenario['recordings']['hr']['timeseries']]
                    # wave_dict[subject_id]['spo2'] = [spo2[:] for spo2 in scenario['recordings']['spo2']['timeseries']]
                    wave_dict[subject_id]['bp'] = [scenario['recordings']['bp_sys']['value']]
                    wave_dict[subject_id]['bp'].append(scenario['recordings']['bp_dia']['value'])
                    flag_bp = True
            if not flag_bp:
                return None

        return wave_dict


def read_video(video_file, config):
    if config.DATA.DATASET in ["vv100", "vv250"]:
        VidObj = cv2.VideoCapture(video_file)
        VidObj.set(cv2.CAP_PROP_POS_MSEC, 0)
        success, frame = VidObj.read()
        frames = []
        while success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.array(frame)
            frames.append(frame)
            success, frame = VidObj.read()
        return np.asarray(frames)


def face_detection(frame, backend):
    """Face detection on a single frame.

    Args:
        frame(np.array): a single frame.
        backend(str): backend to utilize for face detection.
        use_larger_box(bool): whether to use a larger bounding box on face detection.
        larger_box_coef(float): Coef. of larger box.
    Returns:
        face_box_coor(List[int]): coordinates of face bouding box.
    """
    if backend == "HC":
        # Use OpenCV's Haar Cascade algorithm implementation for face detection
        # This should only utilize the CPU
        detector = cv2.CascadeClassifier(
            './dataset/haarcascade_frontalface_default.xml')

        # Computed face_zone(s) are in the form [x_coord, y_coord, width, height]
        # (x,y) corresponds to the top-left corner of the zone to define using
        # the computed width and height.
        face_zone = detector.detectMultiScale(frame)

        if len(face_zone) < 1:
            print("ERROR: No Face Detected")
            face_box_coor = [0, 0, frame.shape[0], frame.shape[1]]
        elif len(face_zone) >= 2:
            # Find the index of the largest face zone
            # The face zones are boxes, so the width and height are the same
            max_width_index = np.argmax(face_zone[:, 2])  # Index of maximum width
            face_box_coor = face_zone[max_width_index]
            print("Warning: More than one faces are detected. Only cropping the biggest one.")
        else:
            face_box_coor = face_zone[0]

    elif backend == "FR":
        face_locations = face_recognition.face_locations(frame, 1, model='hog')
        if len(face_locations) == 1:
            (bottom, right, top, left) = face_locations[0]
            face_box_coor = [left, bottom, right - left, top - bottom]
        elif len(face_locations) > 1:
            # Find the index of the largest face zone
            # The face zones are boxes, so the width and height are the same
            max_width_index = np.argmax([face_location[1] - face_location[3] for face_location in face_locations])
            face_locations = face_locations[max_width_index]
            (bottom, right, top, left) = face_locations
            face_box_coor = [left, bottom, right - left, top - bottom]
            print("Warning: More than one faces are detected. Only cropping the biggest one.")
        else:
            print("ERROR: No Face Detected")
            face_box_coor = [0, 0, frame.shape[0], frame.shape[1]]

    else:
        raise ValueError("Unsupported face detection backend!")

    return face_box_coor


def crop_face_resize(frames, backend, width, height):
    """Crop face and resize frames.

    Args:
        frames(np.array): Video frames.
        use_dynamic_detection(bool): If False, all the frames use the first frame's bouding box to crop the faces
                                     and resizing.
                                     If True, it performs face detection every "detection_freq" frames.
        detection_freq(int): The frequency of dynamic face detection e.g., every detection_freq frames.
        width(int): Target width for resizing.
        height(int): Target height for resizing.
        use_larger_box(bool): Whether enlarge the detected bouding box from face detection.
        use_face_detection(bool):  Whether crop the face.
        larger_box_coef(float): the coefficient of the larger region(height and weight),
                            the middle point of the detected region will stay still during the process of enlarging.
    Returns:
        resized_frames(list[np.array(float)]): Resized and cropped frames
    """
    # Face Cropping

    face_region_all = []
    # Perform face detection by num_dynamic_det times.
    face_region_all.append(face_detection(frames[0], backend))
    face_region_all = np.asarray(face_region_all, dtype='int')

    # Frame Resizing
    resized_frames = np.zeros((frames.shape[0], height, width, 3))
    for i in tqdm(range(0, frames.shape[0]), desc="cropping and resizing", position=1, leave=False):
        frame = frames[i]
        face_region = face_region_all[0]
        frame = frame[max(face_region[1], 0):min(face_region[1] + face_region[3], frame.shape[0]),
                max(face_region[0], 0):min(face_region[0] + face_region[2], frame.shape[1])]
        resized_frames[i] = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    return resized_frames


def get_ppg_from_video(frames, fs):
    RGB = []
    for frame in frames:
        summation = np.sum(np.sum(frame, axis=0), axis=0)
        RGB.append(summation / (frame.shape[0] * frame.shape[1]))
    RGB = np.asarray(RGB)
    RGB = Smooth().apply(RGB)
    pred_ppg = pos.POS(RGB, fs)
    pred_ppg = Detrend().apply(pred_ppg)
    pred_ppg = BandpassFilter(filter_type="butterworth", fs=30, low=0.75, high=2.5).apply(pred_ppg)

    hilbert_ppg = HilbertNormalization().apply(pred_ppg)
    signal = np.expand_dims(hilbert_ppg, 0)
    N = next_power_of_2(signal.shape[1])
    f_ppg, pxx_ppg = scipy.signal.periodogram(signal, fs=fs, nfft=N, detrend=False)
    pxx_ppg = pxx_ppg.squeeze()

    # get hr range
    f_ppg = f_ppg.squeeze()
    fmask_ppg = np.argwhere((f_ppg >= 0.75) & (f_ppg <= 2.5))

    masked_ppg = np.take(f_ppg, fmask_ppg)
    masked_pxx_ppg = np.take(pxx_ppg, fmask_ppg).squeeze()

    masked_fft_hr_ppg = np.take(masked_ppg, np.argmax(masked_pxx_ppg)) * 60

    return RGB, pred_ppg, masked_fft_hr_ppg


def preprocess(config, data_dirs, i):
    if config.DATA.DATASET in ["vv100", "vv250"]:
        wave_file = data_dirs[i]['path']
        wave_dict = read_wave(wave_file, config)
        if wave_dict is None:
            return None
        subject_id = list(wave_dict.keys())[0]
        video_file = os.path.join(config.DATA.DATASET_PATH, wave_dict[subject_id]['video'])
        frames = read_video(video_file, config)
    else:
        raise ValueError("Unsupported dataset!")

    if len(frames) > 0:
        frames = crop_face_resize(frames=frames, backend="FR", width=72, height=72)
        data = []
        for i in range(len(frames) // 600):
            RGB, pred_ppg, pred_hr = get_ppg_from_video(frames[i * 600:(i + 1) * 600], 30)
            data.append(
                {'rgb': RGB, 'ppg': pred_ppg, 'hr': pred_hr, 'bp': wave_dict[subject_id]['bp'],
                 'age': wave_dict[subject_id]['age'],
                 'gender': wave_dict[subject_id]['gender']})
        return data
    else:
        return None


def save_data_to_hdf5(dataset_name, subject_id, rgb, ppg, hr, age, gender, bp,
                      base_directory=""):
    if os.path.isdir(base_directory) is False:
        os.makedirs(base_directory)

    file_name = f"{base_directory}/{dataset_name}_subject_{subject_id}.hdf5"

    with h5py.File(file_name, 'w') as f:
        # Convert the data and labels to numpy arrays
        rgb_array = np.array(rgb)
        ppg_array = np.array(ppg)
        gender_array = np.array(gender)
        bp_array = np.array(bp)

        # Create datasets for the data and labels
        f.create_dataset('rgb', data=rgb_array, compression='gzip')
        f.create_dataset('ppg', data=ppg_array, compression='gzip')
        f.create_dataset('hr', data=hr)
        f.create_dataset('age', data=age)
        f.create_dataset('gender', data=gender_array, compression='gzip')
        f.create_dataset('bp', data=bp_array, compression='gzip')


if __name__ == '__main__':
    conf = config.load_config('config.yaml')
    # Load dataset
    data_dirs = get_raw_data(conf)
    data_dirs.sort(key=lambda x: x['index'])
    pbar = tqdm(range(len(data_dirs)))

    for i in pbar:
        pbar.set_description(f"preprocessing {i}:{data_dirs[i]['subject']}")
        preprocessed_data = preprocess(conf, data_dirs, i)
        if preprocessed_data is None:
            continue
        for data in preprocessed_data:
            save_data_to_hdf5(conf.DATA.DATASET, data_dirs[i]['subject'], data['rgb'], data['ppg'], data['hr'],
                              data['age'], data['gender'], data['bp'], conf.DATA.PREPROCESSED_PATH)
