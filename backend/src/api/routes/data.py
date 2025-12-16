"""
Data API Routes
Endpoints for heatmap data and metadata retrieval.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ...services.data_loader import get_cache
from ...utils.config import VALID_MONTHS, VALID_METRICS
from ..models.response import (
    HeatmapResponse,
    HeatmapDataPoint,
    MetadataResponse,
    MetricOption,
    DataCoverage
)

router = APIRouter()


@router.get("/heatmap", response_model=HeatmapResponse)
async def get_heatmap_data(
    month: Optional[int] = Query(202412, description="Month identifier in YYYYMM format"),
    hour: Optional[int] = Query(0, description="Hour of day (0-23)", ge=0, le=23),
    metric: Optional[str] = Query("avg_total_users", description="User duration metric to visualize"),
    day_type: Optional[str] = Query("平日", description="Day type (平日 or 假日)")
):
    """
    Get heatmap data for specific time period.

    Retrieves location data points with user counts for visualization on a map.
    Returns geographic coordinates (lat/lng) and weight values for the selected
    month, hour, metric, and day_type combination.

    - **month**: Month identifier in YYYYMM format (202412, 202502, 202505, 202508)
    - **hour**: Hour of day (0-23, 24-hour format)
    - **metric**: User duration metric to visualize
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
        cache = get_cache()
        data = cache.get_heatmap_data(month, hour, metric, day_type)

        if not data:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for month={month}, hour={hour}"
            )

        # Calculate min/max weights
        weights = [point['weight'] for point in data]
        min_weight = min(weights) if weights else 0
        max_weight = max(weights) if weights else 0

        # Convert to response model
        data_points = [HeatmapDataPoint(**point) for point in data]

        return HeatmapResponse(
            month=month,
            hour=hour,
            metric=metric,
            count=len(data_points),
            min_weight=min_weight,
            max_weight=max_weight,
            data=data_points
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/metadata", response_model=MetadataResponse)
async def get_metadata():
    """
    Get system metadata.

    Returns available months, hours, metrics, and data statistics.
    Used by frontend to populate dropdown options and validate selections.
    """
    try:
        cache = get_cache()
        metadata = cache.get_metadata()

        # Convert to response model
        return MetadataResponse(
            months=metadata['months'],
            hours=metadata['hours'],
            metrics=[MetricOption(**m) for m in metadata['metrics']],
            total_locations=metadata['total_locations'],
            data_coverage=DataCoverage(**metadata['data_coverage'])
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
