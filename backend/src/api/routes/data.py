"""
Data API Routes
Endpoints for heatmap data and metadata retrieval.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ...services.data_loader import get_cache
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

    - **month**: Month identifier in YYYYMM format
    - **hour**: Hour of day (0-23, 24-hour format)
    - **metric**: User duration metric to visualize
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

        data = cache.get_heatmap_data(month, hour, metric, day_type)

        if not data:
            # Use 200 OK with empty data list instead of 404
            # A lack of data for a valid time period is not a client error
            return HeatmapResponse(
                month=month,
                hour=hour,
                metric=metric,
                count=0,
                min_weight=0,
                max_weight=0,
                data=[]
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

    except Exception as e:
        # Catch-all for unexpected errors, e.g., cache not initialized
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
