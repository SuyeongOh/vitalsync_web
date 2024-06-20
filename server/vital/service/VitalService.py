import asyncio
from datetime import datetime

import numpy as np
from fastapi import FastAPI, HTTPException, status

from server.vital.analysis.vital_calculator import VitalCalculator
from server.vital.analysis.core.ppg import pos
from server.vital.db.ground_truth import GtResponse, GtRequest
from server.vital.db.vital import VitalRequest, VitalResponse
from server.vital.pipeline_package import preprocess_pipeline
from server.vital.service import DataService

vitalService = FastAPI()


# gender : male-남자, female-여자
@vitalService.post("/vital/all", response_model=VitalResponse)
async def calculate_vital(vital_request: VitalRequest):
    if not vital_request.RGB:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid RGB data.")

    # 계산된 결과를 반환합니다. 실제 애플리케이션에서는 계산 로직에 따라 결과가 달라질 것입니다.

    # Calculate PPG
    RGB = np.asarray(vital_request.RGB).transpose(1, 0)
    RGB = preprocess_pipeline.apply(RGB)

    # Calculate PPG
    pred_ppg = pos.POS(RGB, 30)

    # Calculate Vital
    vitalcalc = VitalCalculator(pred_ppg, 30)
    fft_hr = vitalcalc.calc_fft_hr()
    ibi_hr = vitalcalc.calc_ibi_hr()
    hrv = vitalcalc.calc_hrv()
    stress = vitalcalc.calc_baevsky_stress_index()
    #stress = vitalcalc.calc_lfhf()
    spo2 = vitalcalc.calc_spo2(RGB)
    #sbp, dbp = vitalcalc.calc_bp(vital_request.height, vital_request.weight, vital_request.age, vital_request.gender)
    mbp = vitalcalc.calc_mbp(RGB, fft_hr, vital_request.age, vital_request.gender)
    sbp = mbp + 13
    dbp = mbp - 26
    br = vitalcalc.calc_br()
    print(f"date: {vital_request.measureTime}\n"
          f"fft_hr: {fft_hr:.2f}, ibi_hr: {ibi_hr:.2f}, hrv: {hrv:.2f}\n"
          f"lf_hf_ratio: {stress:.2f}, spo2: {spo2:.2f}\n"
          f"gender: {vital_request.gender}, age: {vital_request.age}, height: {vital_request.height}, weight: {vital_request.weight}\n"
          f"sbp: {sbp:.2f}, dbp: {dbp:.2f}, bp: {sbp*0.33 + dbp*0.66:.2f}\n"
          f"br: {br:.2f}\n")

    response = VitalResponse(
        hr=fft_hr,
        ibi_hr=ibi_hr,
        hrv=hrv,
        rr=br,
        spo2=spo2,
        stress=stress,
        bp=mbp,
        sbp=sbp,
        dbp=dbp,
        status=200,
        message="Success"
    )
    if not vital_request.id == "Guest":
        currentTime = vital_request.measureTime
        ppg_blob = vitalcalc.ppg.tobytes()
        r = vital_request.RGB.pop(0)
        g = vital_request.RGB.pop(0)
        b = vital_request.RGB.pop(0)
        await asyncio.create_task(DataService.savePpgSignal(vital_request.id, ppg_blob, r, g, b, currentTime))
        await asyncio.create_task(DataService.saveData(vital_request.id, response, currentTime))
        # saveGTdata
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


@vitalService.post("/vital/gt", response_model=GtResponse)
def postGT(gt_request: GtRequest):
    response = DataService.saveGt(gt_request)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(vitalService, host="0.0.0.0", port=1024)
