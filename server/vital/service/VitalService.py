from datetime import datetime

import numpy as np
from fastapi import FastAPI, HTTPException, status

from server.vital.analysis.vital_calculator import VitalCalculator
from server.vital.core import pos
from server.vital.pipeline_package import preprocess_pipeline
from server.vital.service import DataService
from server.vital.service.models import VitalRequest, VitalResponse

vitalService = FastAPI()


@vitalService.post("/vital/all", response_model=VitalResponse)
async def calculate_vital(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    today = datetime.today().strftime("%Y%m%d")
    time = datetime.now().strftime("%H%M%S")
    # preprocess RGB data
    RGB = np.asarray(vital_request.RGB).transpose(1, 0)
    RGB = preprocess_pipeline.apply(RGB)

    # Calculate PPG
    pred_ppg = pos.POS(RGB, 30)

    # Calculate Vital
    vitalcalc = VitalCalculator(pred_ppg, 30)
    fft_hr = vitalcalc.calc_fft_hr()
    ibi_hr = vitalcalc.calc_ibi_hr()
    hrv = vitalcalc.calc_hrv()
    hrv_confidence = vitalcalc.calc_hrv_confidence()
    lf_hf_ratio = vitalcalc.calc_lfhf()
    spo2 = vitalcalc.calc_spo2(RGB)
    print(f"date: {today}, time: {time}\n"
          f"fft_hr: {fft_hr:.2f}, ibi_hr: {ibi_hr:.2f}, hrv: {hrv:.2f}\n"
          f"hrv confidence: {hrv_confidence*100:.2f}%\n"
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

    currentTime = DataService.get_current_time_str()
    await DataService.savePpgSignal(vital_request.id, vitalcalc.ppg, currentTime)
    await DataService.saveData(vital_request.id, response, currentTime)
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
