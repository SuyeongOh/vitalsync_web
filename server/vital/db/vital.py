from pydantic import BaseModel
from typing import List, Optional


class VitalRequest(BaseModel):
    RGB: List[List[float]]
    age: int = 0
    bmi: float = 20.1
    weight: float = 0
    height: float = 0
    gender: str = "male"
    id: Optional[str] = None
    measureTime: str = "0"

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
