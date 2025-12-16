"""
Demographics API Routes
Endpoints for demographic statistics retrieval.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from functools import lru_cache

from ...services.data_loader import get_cache
from ..models.response import (
    DemographicResponse,
    Demographics,
    GenderDistribution,
    AgeDistribution
)

router = APIRouter()


@lru_cache(maxsize=128)
def _get_demographics_cached(month: int, hour: int, metric: str, day_type: str) -> dict:
    """
    Cached demographic calculation.

    LRU cache improves performance for frequently accessed time periods.
    """
    cache = get_cache()
    return cache.get_demographics(month, hour, metric, day_type)


@router.get("/demographics", response_model=DemographicResponse)
async def get_demographics(
    month: Optional[int] = Query(202412, description="Month identifier in YYYYMM format"),
    hour: Optional[int] = Query(0, description="Hour of day (0-23)", ge=0, le=23),
    metric: Optional[str] = Query("avg_total_users", description="Metric to use for weighting"),
    day_type: Optional[str] = Query("平日", description="Day type (平日 or 假日)")
):
    """
    Get demographic statistics for specific time period.

    Retrieves aggregated demographic statistics (gender and age distribution)
    for the selected month, hour, and day_type. Percentages are weighted by the selected
    metric to reflect actual user distribution.

    - **month**: Month identifier in YYYYMM format
    - **hour**: Hour of day (0-23)
    - **metric**: Metric to use for weighting demographic calculations
    - **day_type**: Day type (平日 or 假日)
    """
    try:
        cache = get_cache()
        
        # Get available options from cache for validation
        metadata = cache.get_metadata()
        available_months = metadata['months']
        available_hours = metadata['hours']
        available_day_types = metadata['day_types']
        available_metrics = [m['key'] for m in metadata['metrics']]

        # Validate inputs against live data
        if month not in available_months:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid month: {month}. Available: {available_months}"
            )
        if hour not in available_hours:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid hour: {hour}. Available: {available_hours}"
            )
        if metric not in available_metrics:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid metric: {metric}. Available: {available_metrics}"
            )
        if day_type not in available_day_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid day_type: {day_type}. Available: {available_day_types}"
            )
        
        # Use cached calculation
        demo_data = _get_demographics_cached(month, hour, metric, day_type)

        if demo_data['total_users'] == 0:
            # Return empty but valid response instead of 404
            return DemographicResponse(
                month=month,
                hour=hour,
                metric=metric,
                total_users=0,
                demographics=Demographics(
                    gender=GenderDistribution(male=0, female=0),
                    age=AgeDistribution()
                )
            )

        # Convert to response model
        return DemographicResponse(
            month=month,
            hour=hour,
            metric=metric,
            total_users=demo_data['total_users'],
            demographics=Demographics(
                gender=GenderDistribution(**demo_data['gender']),
                age=AgeDistribution(
                    under_19=demo_data['age'].get('age_1', 0),
                    age_20_24=demo_data['age'].get('age_2', 0),
                    age_25_29=demo_data['age'].get('age_3', 0),
                    age_30_34=demo_data['age'].get('age_4', 0),
                    age_35_39=demo_data['age'].get('age_5', 0),
                    age_40_44=demo_data['age'].get('age_6', 0),
                    age_45_49=demo_data['age'].get('age_7', 0),
                    age_50_54=demo_data['age'].get('age_8', 0),
                    age_55_59=demo_data['age'].get('age_9', 0),
                    age_60_plus=demo_data['age'].get('age_other', 0)
                )
            )
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
