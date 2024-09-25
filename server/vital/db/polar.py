from typing import List, Optional
from pydantic import BaseModel

class PolarRequest(BaseModel):
    ppg_signal: List[int]
    ecg_signal: List[int]
    id: str = ""
    measurementTime = 0


class PolarResponse(BaseModel):
    status: int = 200
    message: str = "Success"
