from pydantic import BaseModel
from typing import List, Optional


class VitalRequest(BaseModel):
    RGB: List[List[float]]
    id: Optional[str] = None
    measureTime = "0"

class VitalResponse(BaseModel):
    hr: float = 0.0
    ibi_hr: float = 0.0
    hrv: float = 0.0
    rr: float = 0.0
    spo2: float = 0.0
    stress: float = 0.0
    bp: float = 0.0
    sbp: float = 0.0
    dbp: float = 0.0
    status: int = 200
    message: str = "Success"
