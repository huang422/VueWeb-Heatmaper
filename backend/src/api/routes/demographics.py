"""
Demographics API Routes
Endpoints for demographic statistics retrieval.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from functools import lru_cache

from ...services.data_loader import get_cache
from ...utils.config import VALID_MONTHS, VALID_METRICS
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

    - **month**: Month identifier in YYYYMM format (202412, 202502, 202505, 202508)
    - **hour**: Hour of day (0-23)
    - **metric**: Metric to use for weighting demographic calculations
    - **day_type**: Day type (平日 or 假日)
    """
    # Validate inputs
    if month not in VALID_MONTHS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid month: must be one of {VALID_MONTHS}"
        )

    if metric not in VALID_METRICS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid metric: must be one of {VALID_METRICS}"
        )

    try:
        # Use cached calculation
        demo_data = _get_demographics_cached(month, hour, metric, day_type)

        if demo_data['total_users'] == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for month={month}, hour={hour}"
            )

        # Convert to response model
        gender = GenderDistribution(
            male=demo_data['gender']['male'],
            female=demo_data['gender']['female']
        )

        age = AgeDistribution(
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

        return DemographicResponse(
            month=month,
            hour=hour,
            metric=metric,
            total_users=demo_data['total_users'],
            demographics=Demographics(gender=gender, age=age)
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
