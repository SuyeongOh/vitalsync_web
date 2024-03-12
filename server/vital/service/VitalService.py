from datetime import datetime

from fastapi import FastAPI, HTTPException, status

from server.vital.analysis.vital_calculator import VitalCalculator
from server.vital.core import pos, omit
from server.vital.pipeline_package import preprocess_pipeline
from server.vital.service import DataService
from server.vital.service.models import VitalRequest, VitalResponse
from server.vital.analysis.visualizer import *

vitalService = FastAPI()


@vitalService.post("/vital/all", response_model=VitalResponse)
async def calculate_vital(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.

    # 여기다가 코드 구현해서 넣으면 된단다.
    today = datetime.today().strftime("%Y%m%d")
    time = datetime.now().strftime("%H%M%S")
    save_dict = {'save_root_path': f'/home/najy/shared_innopia/test_results/{today}/',
                 'name': f"test_{time}",
                 'model': 'POS', 'seq_num': 0, 'desc': 'Original RGB', 'show_flag': False, 'plot_peak': False,
                 'figsize': (8, 9), 'fontsize': 10,
                 'norm_flag': True, 'diff_flag': False}

    # Calculate PPG
    RGB = np.asarray(vital_request.RGB).transpose(1, 0)
    rgb_plot(RGB, save_dict)

    RGB = preprocess_pipeline.apply(RGB, save_dict)
    save_dict['desc'] = 'Smoothed RGB'
    save_dict['seq_num'] += 1
    rgb_plot(RGB, save_dict)

    if save_dict['model'] == 'POS':
        pred_ppg = pos.POS(RGB, 30)
    elif save_dict['model'] == 'OMIT':
        pred_ppg = omit.OMIT(RGB)
    else:
        raise ValueError(f"Invalid model name: {save_dict['model']}")
    save_dict['show_flag'] = True
    bvp_fft_plot(pred_ppg, 30, save_dict)

    # Calculate Vital
    vitalcalc = VitalCalculator(pred_ppg, 30, save_dict)
    fft_hr = vitalcalc.calc_fft_hr()
    ibi_hr = vitalcalc.calc_ibi_hr()
    hrv = vitalcalc.calc_hrv()
    lf_hf_ratio = vitalcalc.calc_lfhf()
    spo2 = vitalcalc.calc_spo2(RGB)
    print(f"date: {today}, time: {time}\n"
          f"fft_hr: {fft_hr:.2f}, ibi_hr: {ibi_hr:.2f}, hrv: {hrv:.2f} "
          f"hrv confidence: {np.exp(-abs(fft_hr - ibi_hr) / 20)*100:.2f}%\n"
          f"lf_hf_ratio: {lf_hf_ratio:.2f}, spo2: {spo2:.2f}")

    response = VitalResponse(
        hr=fft_hr,
        hrv=hrv,
        rr=16.0,
        spo2=spo2,
        stress=lf_hf_ratio,
        bp=120.75,
        sbp=120.0,
        dbp=80.0,
        status=200,
        message="Success"
    )
    await DataService.saveData(vital_request.id, response)
    # asyncio.run(DataService.saveData(vital_request.id, response))

    return response


@vitalService.post("/vital/hr", response_model=VitalResponse)
def calculate_hr(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.
    hr = 0
    # 여기다가 코드 구현해서 넣으면 된단다.
    response = VitalResponse(
        hr=72.0,
        status=200,
        message="Success"
    )
    return response


@vitalService.post("/vital/hrv", response_model=VitalResponse)
def calculate_hrv(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.
    hrv = 0
    # 여기다가 코드 구현해서 넣으면 된단다.
    response = VitalResponse(
        hrv=50.0,
        status=200,
        message="Success"
    )
    return response


@vitalService.post("/vital/rr", response_model=VitalResponse)
def calculate_rr(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.
    rr = 0
    # 여기다가 코드 구현해서 넣으면 된단다.
    response = VitalResponse(
        rr=12.0,
        status=200,
        message="Success"
    )
    return response


@vitalService.post("/vital/spo2", response_model=VitalResponse)
def calculate_spo2(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.
    spo2 = 0
    # 여기다가 코드 구현해서 넣으면 된단다.
    response = VitalResponse(
        spo2=72.0,
        status=200,
        message="Success"
    )
    return response


@vitalService.post("/vital/stress", response_model=VitalResponse)
def calculate_stress(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.
    stress = 0
    # 여기다가 코드 구현해서 넣으면 된단다.
    response = VitalResponse(
        stress=72.0,
        status=200,
        message="Success"
    )
    return response


@vitalService.post("/vital/bp", response_model=VitalResponse)
def calculate_bp(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.

    # 여기다가 코드 구현해서 넣으면 된단다.
    response = VitalResponse(
        bp=101.9,
        sbp=133.0,
        dbp=80.0,
        status=200,
        message="Success"
    )
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(vitalService, host="0.0.0.0", port=1024)
