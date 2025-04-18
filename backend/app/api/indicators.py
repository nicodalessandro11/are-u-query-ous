from fastapi import APIRouter, Depends
from app.schemas.indicator import IndicatorQuery, IndicatorResponse

router = APIRouter()

@router.get("/", response_model=IndicatorResponse)
def get_indicators(params: IndicatorQuery = Depends()):
    # Normalmente acá irías a buscar datos a Supabase
    return {
        "indicator": "income",
        "value": 28100,
        "unit": "€",
        "year": params.year or 2023,
        "geo_name": f"{params.geo_level.capitalize()} {params.geo_id}"
    }
