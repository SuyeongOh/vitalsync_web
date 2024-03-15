from pydantic import BaseModel
from typing import List, Optional


class GtRequest(BaseModel):
    hr: float = 0.0
    hrv: float = 0.0
    rr: float = 0.0
    spo2: float = 0.0
    stress: float = 0.0
    sbp: float = 0.0
    dbp: float = 0.0
    measureTime = ""
    id: Optional[str] = None


class GtResponse(BaseModel):

    status: int = 200
    message: str = "Success"
