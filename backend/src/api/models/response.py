"""
API Response Models
Pydantic schemas matching OpenAPI specification.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class HeatmapDataPoint(BaseModel):
    """Single location data point for heatmap visualization."""
    gx: int = Field(..., description="Grid X coordinate (Taiwan TWD97 TM2 system)")
    gy: int = Field(..., description="Grid Y coordinate (Taiwan TWD97 TM2 system)")
    lat: float = Field(..., description="WGS84 latitude in decimal degrees")
    lng: float = Field(..., description="WGS84 longitude in decimal degrees")
    weight: float = Field(..., description="User count for selected metric at this location", ge=0)


class HeatmapResponse(BaseModel):
    """Response containing heatmap data for a specific time period."""
    month: int = Field(..., description="Month identifier (YYYYMM)")
    hour: int = Field(..., description="Hour of day (0-23)", ge=0, le=23)
    metric: str = Field(..., description="Selected user duration metric")
    count: int = Field(..., description="Number of location data points returned", ge=0)
    min_weight: float = Field(..., description="Minimum weight value in dataset")
    max_weight: float = Field(..., description="Maximum weight value in dataset")
    data: List[HeatmapDataPoint] = Field(..., description="Array of location data points")

    class Config:
        json_schema_extra = {
            "example": {
                "month": 202412,
                "hour": 14,
                "metric": "avg_total_users",
                "count": 245,
                "min_weight": 0.5,
                "max_weight": 150.3,
                "data": [
                    {
                        "gx": 7165,
                        "gy": 7152,
                        "lat": 25.033311,
                        "lng": 121.543653,
                        "weight": 20.67
                    },
                    {
                        "gx": 7166,
                        "gy": 7152,
                        "lat": 25.033789,
                        "lng": 121.544201,
                        "weight": 41.89
                    }
                ]
            }
        }


class GenderDistribution(BaseModel):
    """Gender distribution percentages."""
    male: float = Field(..., description="Percentage of male users (男性)", ge=0, le=100)
    female: float = Field(..., description="Percentage of female users (女性)", ge=0, le=100)


class AgeDistribution(BaseModel):
    """Age group distribution percentages."""
    under_19: float = Field(..., description="Percentage of users 19歲以下", ge=0, le=100)
    age_20_24: float = Field(..., description="Percentage of users 20-24歲", ge=0, le=100)
    age_25_29: float = Field(..., description="Percentage of users 25-29歲", ge=0, le=100)
    age_30_34: float = Field(..., description="Percentage of users 30-34歲", ge=0, le=100)
    age_35_39: float = Field(..., description="Percentage of users 35-39歲", ge=0, le=100)
    age_40_44: float = Field(..., description="Percentage of users 40-44歲", ge=0, le=100)
    age_45_49: float = Field(..., description="Percentage of users 45-49歲", ge=0, le=100)
    age_50_54: float = Field(..., description="Percentage of users 50-54歲", ge=0, le=100)
    age_55_59: float = Field(..., description="Percentage of users 55-59歲", ge=0, le=100)
    age_60_plus: float = Field(..., description="Percentage of users 60+ (age_other)", ge=0, le=100)


class Demographics(BaseModel):
    """Complete demographic breakdown."""
    gender: GenderDistribution
    age: AgeDistribution


class DemographicResponse(BaseModel):
    """Response containing demographic statistics."""
    month: int = Field(..., description="Month identifier (YYYYMM)")
    hour: int = Field(..., description="Hour of day (0-23)", ge=0, le=23)
    metric: str = Field(..., description="Metric used for weighting")
    total_users: float = Field(..., description="Total user count across all locations for this time period")
    demographics: Demographics

    class Config:
        json_schema_extra = {
            "example": {
                "month": 202412,
                "hour": 14,
                "metric": "avg_total_users",
                "total_users": 5234.5,
                "demographics": {
                    "gender": {
                        "male": 54.2,
                        "female": 45.8
                    },
                    "age": {
                        "under_19": 2.1,
                        "age_20_24": 6.8,
                        "age_25_29": 9.3,
                        "age_30_34": 8.2,
                        "age_35_39": 7.5,
                        "age_40_44": 8.1,
                        "age_45_49": 10.2,
                        "age_50_54": 11.4,
                        "age_55_59": 12.3,
                        "age_60_plus": 24.1
                    }
                }
            }
        }


class MetricOption(BaseModel):
    """Metric option with key and label."""
    key: str = Field(..., description="Metric identifier")
    label: str = Field(..., description="Human-readable label (Chinese)")


class DataCoverage(BaseModel):
    """Data coverage statistics."""
    total_data_points: int = Field(..., description="Total number of rows in dataset")
    unique_locations: int = Field(..., description="Number of unique (gx, gy) locations")
    time_periods: int = Field(..., description="Number of unique (month, hour) combinations")


class MetadataResponse(BaseModel):
    """System metadata and available options."""
    months: List[int] = Field(..., description="Available months")
    hours: List[int] = Field(..., description="Available hours (0-23)")
    metrics: List[MetricOption] = Field(..., description="Available user duration metrics")
    total_locations: int = Field(..., description="Total number of data points in dataset")
    data_coverage: DataCoverage

    class Config:
        json_schema_extra = {
            "example": {
                "months": [202412, 202502, 202505, 202508],
                "hours": list(range(24)),
                "metrics": [
                    {"key": "avg_total_users", "label": "全部停留人數"},
                    {"key": "avg_users_under_10min", "label": "停留10分鐘以下"},
                    {"key": "avg_users_10_30min", "label": "停留10-30分鐘"},
                    {"key": "avg_users_over_30min", "label": "停留30分鐘以上"}
                ],
                "total_locations": 2881,
                "data_coverage": {
                    "total_data_points": 2881,
                    "unique_locations": 547,
                    "time_periods": 96
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response."""
    detail: str = Field(..., description="Error message")
