"""
Location Data Models
Defines data structures for location points with demographics.
"""

from typing import Optional
from pydantic import BaseModel, Field


class LocationPoint(BaseModel):
    """
    Represents user activity at a specific grid location for a specific time.

    Attributes map to CSV columns and coordinate conversion results.
    """
    month: int = Field(..., description="Month identifier in YYYYMM format", ge=202401, le=209912)
    gx: int = Field(..., description="Grid X coordinate (TWD97 TM2 system)", ge=0, le=10000)
    gy: int = Field(..., description="Grid Y coordinate (TWD97 TM2 system)", ge=0, le=10000)
    lat: float = Field(..., description="WGS84 latitude (degrees)", ge=21.9, le=25.3)
    lng: float = Field(..., description="WGS84 longitude (degrees)", ge=118.0, le=122.1)
    hour: int = Field(..., description="Hour of day (24-hour format)", ge=0, le=23)
    day_type: Optional[str] = Field(None, description="Weekday/Weekend classification")

    # Metrics
    avg_total_users: float = Field(..., description="Average total users", ge=0)
    avg_users_under_10min: Optional[float] = Field(None, description="Average users <10min", ge=0)
    avg_users_10_30min: Optional[float] = Field(None, description="Average users 10-30min", ge=0)
    avg_users_over_30min: Optional[float] = Field(None, description="Average users >30min", ge=0)

    # Demographics - Gender
    sex_1: Optional[float] = Field(None, description="Male percentage", ge=0, le=100)
    sex_2: Optional[float] = Field(None, description="Female percentage", ge=0, le=100)

    # Demographics - Age
    age_1: Optional[float] = Field(None, description="Age 19以下 percentage", ge=0, le=100)
    age_2: Optional[float] = Field(None, description="Age 20-24 percentage", ge=0, le=100)
    age_3: Optional[float] = Field(None, description="Age 25-29 percentage", ge=0, le=100)
    age_4: Optional[float] = Field(None, description="Age 30-34 percentage", ge=0, le=100)
    age_5: Optional[float] = Field(None, description="Age 35-39 percentage", ge=0, le=100)
    age_6: Optional[float] = Field(None, description="Age 40-44 percentage", ge=0, le=100)
    age_7: Optional[float] = Field(None, description="Age 45-49 percentage", ge=0, le=100)
    age_8: Optional[float] = Field(None, description="Age 50-54 percentage", ge=0, le=100)
    age_9: Optional[float] = Field(None, description="Age 55-59 percentage", ge=0, le=100)
    age_other: Optional[float] = Field(None, description="Age 60+ percentage", ge=0, le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "month": 202412,
                "gx": 7165,
                "gy": 7152,
                "lat": 25.033311,
                "lng": 121.543653,
                "hour": 0,
                "day_type": "假日",
                "avg_total_users": 20.67,
                "avg_users_under_10min": 1.0,
                "avg_users_10_30min": 7.0,
                "avg_users_over_30min": 12.67,
                "sex_1": 54.42,
                "sex_2": 45.58,
                "age_1": 1.43,
                "age_2": 3.49,
                "age_3": 6.68,
                "age_4": 6.59,
                "age_5": 11.90,
                "age_6": 4.84,
                "age_7": 11.92,
                "age_8": 8.46,
                "age_9": 17.43,
                "age_other": 27.27
            }
        }
