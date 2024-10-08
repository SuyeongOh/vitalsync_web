import json
import pickle
import base64

import numpy as np

from server.vital.analysis.core.ppg import pos, omit
from server.vital.analysis.vital_calculator import VitalCalculator
from server.vital.pipeline_package import preprocess_pipeline


# Step 1: JSON 파일 읽기
def load_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


# Step 2: "b_signal" 필드 데이터 디코딩하기
def decode_blob(blob):
    # Base64 디코딩
    decoded_blob = base64.b64decode(blob)
    # Pickle 언패킹
    unpickled_data = pickle.loads(decoded_blob)
    # numpy array로 변환
    np_array = np.array(unpickled_data)
    return np_array


# Step 3: JSON 데이터 파싱 및 특정 필드 추출
def process_json_data(data):
    results = {}
    for entry in data:
        measurement_time = entry.get("MeasurementTime")
        user_id = entry.get("UserID")
        vital_signal_id = entry.get("VitalSignalID")
        b_signal_blob = entry.get("b_signal")
        g_signal_blob = entry.get("g_signal")
        r_signal_blob = entry.get("r_signal")

        result = {}
        if r_signal_blob:
            try:
                r_signal_data = decode_blob(r_signal_blob)
                result["MeasurementTime"] = measurement_time
                result["UserID"] = user_id
                result["VitalSignalID"] = vital_signal_id
                result["r_signal"] = r_signal_data
            except Exception as e:
                print(f"Error decoding b_signal for entry {measurement_time}: {e}")
        if g_signal_blob:
            try:
                g_signal_data = decode_blob(g_signal_blob)
                result["MeasurementTime"] = measurement_time
                result["UserID"] = user_id
                result["VitalSignalID"] = vital_signal_id
                result["g_signal"] = g_signal_data
            except Exception as e:
                print(f"Error decoding b_signal for entry {measurement_time}: {e}")
        if b_signal_blob:
            try:
                b_signal_data = decode_blob(b_signal_blob)
                result["MeasurementTime"] = measurement_time
                result["UserID"] = user_id
                result["VitalSignalID"] = vital_signal_id
                result["b_signal"] = b_signal_data
            except Exception as e:
                print(f"Error decoding b_signal for entry {measurement_time}: {e}")

        results[user_id + "_" + measurement_time] = (result)
    return results


# Step 4: 결과 출력
filename = 'VitalSignal.json'
json_data = load_json_file(filename)
processed_data = process_json_data(json_data)

test_data = processed_data["ku_014_20241007132649"]
# Calculate PPG
original_RGB = [
    test_data["r_signal"],
    test_data["g_signal"],
    test_data["b_signal"]
]
RGB = np.asarray(original_RGB).transpose(1, 0)
RGB = preprocess_pipeline.apply(RGB)

# Calculate PPG
pred_ppg = omit.OMIT(RGB)
#pred_ppg = pos.POS(RGB, 30)
# Calculate Vital
vitalcalc = VitalCalculator(pred_ppg, 30)
fft_hr = vitalcalc.calc_fft_hr()
ibi_hr = vitalcalc.calc_ibi_hr()
hrv = vitalcalc.calc_hrv()
stress = vitalcalc.calc_baevsky_stress_index()
spo2 = vitalcalc.calc_spo2(original_RGB)
br = vitalcalc.calc_br()
print(f"fft_hr: {fft_hr:.2f}, ibi_hr: {ibi_hr:.2f}, hrv: {hrv:.2f}\n"
      f"lf_hf_ratio: {stress:.2f}, spo2: {spo2:.2f} br: {br:.2f}\n")

