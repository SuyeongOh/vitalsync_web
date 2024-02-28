from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pipeline_package import preprocess_pipeline, postprocess_pipeline
from core import pos, omit
from analysis.vital_calculator import VitalCalculator
import numpy as np
from analysis.visualizer import *
vitalService = FastAPI()


class VitalRequest(BaseModel):
    RGB: List[List[float]]
    id: Optional[str] = None


class VitalResponse(BaseModel):
    hr: float = 0.0
    hrv: float = 0.0
    rr: float = 0.0
    spo2: float = 0.0
    stress: float = 0.0
    bp: float = 0.0
    sbp: float = 0.0
    dbp: float = 0.0
    status: int = 200
    message: str = "Success"


@vitalService.post("/vital/all", response_model=VitalResponse)
def calculate_vital(vital_request: VitalRequest):
    # 여기에서 데이터를 처리하고 결과를 계산하는 로직을 구현합니다.
    # 예제를 위해 임의의 값을 반환하겠습니다.

    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.

    # preprocess RGB data
    RGB = np.asarray(vital_request.RGB).transpose(1, 0)
    RGB = preprocess_pipeline.apply(RGB)

    # Calculate PPG
    pred_ppg = omit.OMIT(RGB)
    pred_ppg = postprocess_pipeline.apply(pred_ppg)

    # Calculate Vital
    vitalcalc = VitalCalculator(pred_ppg, 30)
    fft_hr = vitalcalc.calc_fft_hr()
    ibi_hr = vitalcalc.calc_ibi_hr()
    hrv = vitalcalc.calc_hrv()
    print(f"fft_hr: {fft_hr}, ibi_hr: {ibi_hr}, hrv: {hrv}")
    response = VitalResponse(
        hr=fft_hr,
        hrv=hrv,
        rr=16.0,
        spo2=98.5,
        stress=14.3,
        bp=120.75,
        sbp=120.0,
        dbp=80.0,
        status=200,
        message="Success"
    )
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
