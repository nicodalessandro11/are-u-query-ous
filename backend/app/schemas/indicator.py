from pydantic import BaseModel
from typing import Optional

class IndicatorQuery(BaseModel):
    geo_level: str
    geo_id: int
    year: Optional[int] = None

class IndicatorResponse(BaseModel):
    indicator: str
    value: float
    unit: str
    year: int
    geo_name: str