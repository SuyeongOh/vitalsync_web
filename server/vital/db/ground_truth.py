from typing import Optional

from pydantic import BaseModel


class GtRequest(BaseModel):
    hr: float = 0.0
    hrv: float = 0.0
    rr: float = 0.0
    spo2: float = 0.0
    stress: float = 0.0
    sbp: float = 0.0
    dbp: float = 0.0
    measureTime: str = "0"
    id: str = ""


class GtResponse(BaseModel):
    status: int = 200
    message: str = "Success"
