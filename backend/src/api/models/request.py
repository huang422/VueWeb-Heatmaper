"""
API Request Models
Pydantic schemas for request validation.
"""

from typing import Optional
from pydantic import BaseModel, Field


class HeatmapRequest(BaseModel):
    """Request parameters for heatmap data."""
    month: Optional[int] = Field(
        202412,
        description="Month identifier in YYYYMM format",
        examples=[202412, 202502, 202505, 202508]
    )
    hour: Optional[int] = Field(
        0,
        description="Hour of day (0-23)",
        ge=0,
        le=23
    )
    metric: Optional[str] = Field(
        "avg_total_users",
        description="User duration metric to visualize",
        examples=["avg_total_users", "avg_users_under_10min", "avg_users_10_30min", "avg_users_over_30min"]
    )


class DemographicRequest(BaseModel):
    """Request parameters for demographic statistics."""
    month: Optional[int] = Field(
        202412,
        description="Month identifier in YYYYMM format",
        examples=[202412, 202502, 202505, 202508]
    )
    hour: Optional[int] = Field(
        0,
        description="Hour of day (0-23)",
        ge=0,
        le=23
    )
    metric: Optional[str] = Field(
        "avg_total_users",
        description="Metric to use for weighting demographic calculations",
        examples=["avg_total_users", "avg_users_under_10min", "avg_users_10_30min", "avg_users_over_30min"]
    )
