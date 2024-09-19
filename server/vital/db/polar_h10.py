from typing import List, Optional
from pydantic import BaseModel

class H10Request(BaseModel):
    signal: List[int]
    id: Optional[str] = None
    measureTime: str = "0"


class H10Response(BaseModel):
    status: int = 200
    message: str = "Success"
