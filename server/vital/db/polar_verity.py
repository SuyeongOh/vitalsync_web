from typing import List, Optional
from pydantic import BaseModel

class VerityRequest(BaseModel):
    PPG: List[float]
    id: Optional[str] = None
    measureTime: str = "0"


class VerityResponse(BaseModel):
    status: int = 200
    message: str = "Success"
