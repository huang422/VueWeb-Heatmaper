"""
Data Loader Service
Loads and caches CSV data with coordinate conversion for the heatmap visualization.

Implements eager coordinate conversion on startup and O(1) lookup via dictionary indexing.
Memory footprint: ~5MB for ~2,881 rows with optimized data types.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from .coordinate_converter import batch_gxgy_to_latlon

logger = logging.getLogger(__name__)


class DataCache:
    """
    In-memory cache for location data with pre-computed coordinates.

    Loads CSV data once on initialization, converts all gx/gy to lat/lng,
    and builds lookup dictionaries for O(1) query performance.
    """

    def __init__(self, csv_path: str):
        """
        Initialize the data cache from CSV file.

        Args:
            csv_path: Path to data.csv file

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV is missing required columns
        """
        self.df: Optional[pd.DataFrame] = None
        self.lookup_dict: Dict[Tuple[int, int, str], pd.DataFrame] = {}
        self.available_months: List[int] = []
        self.available_hours: List[int] = []
        self.available_day_types: List[str] = []
        self.metrics: List[str] = [
            "avg_total_users",
            "avg_users_under_10min",
            "avg_users_10_30min",
            "avg_users_over_30min"
        ]

        self._load_data(csv_path)

    def _load_data(self, csv_path: str):
        """Load CSV and perform all preprocessing."""
        csv_file = Path(csv_path)
        if not csv_file.exists():
            raise FileNotFoundError(f"Data file not found: {csv_path}")

        logger.info(f"Loading data from {csv_path}...")

        # Load CSV with optimized data types
        dtype_mapping = {
            'month': 'int32',
            'gx': 'int16',
            'gy': 'int16',
            'hour': 'int8',
            'day_type': 'category',
            'avg_total_users': 'float32',
            'avg_users_under_10min': 'float32',
            'avg_users_10_30min': 'float32',
            'avg_users_over_30min': 'float32',
            'sex_1': 'float32',
            'sex_2': 'float32',
            'age_1': 'float32',
            'age_2': 'float32',
            'age_3': 'float32',
            'age_4': 'float32',
            'age_5': 'float32',
            'age_6': 'float32',
            'age_7': 'float32',
            'age_8': 'float32',
            'age_9': 'float32',
            'age_other': 'float32',
        }

        self.df = pd.read_csv(csv_path, dtype=dtype_mapping)
        
        # Validate required columns
        required_cols = ['month', 'gx', 'gy', 'hour', 'day_type'] + self.metrics
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"CSV missing required columns: {missing_cols}")

        logger.info(f"Loaded {len(self.df)} rows")

        # Convert coordinates (EAGER)
        logger.info("Converting gx/gy to lat/lng...")
        lat_array, lng_array = batch_gxgy_to_latlon(
            self.df['gx'].values,
            self.df['gy'].values
        )
        self.df['lat'] = lat_array.astype('float64')
        self.df['lng'] = lng_array.astype('float64')
        logger.info("Coordinate conversion complete")

        # Build metadata
        self.available_months = sorted(self.df['month'].unique().tolist())
        self.available_hours = sorted(self.df['hour'].unique().tolist())
        self.available_day_types = sorted(self.df['day_type'].unique().tolist())

        # Build lookup dictionary for O(1) filtering
        logger.info("Building lookup index...")
        for month in self.available_months:
            for hour in self.available_hours:
                for day_type in self.available_day_types:
                    mask = (self.df['month'] == month) & (self.df['hour'] == hour) & (self.df['day_type'] == day_type)
                    filtered_df = self.df[mask]
                    if not filtered_df.empty:
                        self.lookup_dict[(month, hour, day_type)] = filtered_df

        logger.info(f"Data cache initialized: {len(self.lookup_dict)} time periods")

    def get_heatmap_data(
        self,
        month: int,
        hour: int,
        metric: str = "avg_total_users",
        day_type: str = "平日"
    ) -> List[Dict]:
        """
        Get heatmap data for specific time period and metric.

        Args:
            month: Month identifier (YYYYMM format)
            hour: Hour of day (0-23)
            metric: User duration metric column name
            day_type: Day type ("平日" or "假日")

        Returns:
            List of dictionaries with keys: gx, gy, lat, lng, weight
        """
        # O(1) lookup
        filtered_df = self.lookup_dict.get((month, hour, day_type))
        if filtered_df is None or filtered_df.empty:
            return []

        # Build response
        result = []
        for _, row in filtered_df.iterrows():
            result.append({
                'gx': int(row['gx']),
                'gy': int(row['gy']),
                'lat': float(row['lat']),
                'lng': float(row['lng']),
                'weight': float(row[metric])
            })

        return result

    def get_demographics(
        self,
        month: int,
        hour: int,
        metric: str = "avg_total_users",
        day_type: str = "平日"
    ) -> Dict:
        """
        Get demographic statistics for specific time period.

        Calculates weighted averages based on the selected metric.

        Args:
            month: Month identifier (YYYYMM format)
            hour: Hour of day (0-23)
            metric: Metric to use for weighting
            day_type: Day type ("平日" or "假日")

        Returns:
            Dictionary with gender and age distribution percentages
        """
        # Get filtered data
        filtered_df = self.lookup_dict.get((month, hour, day_type))
        if filtered_df is None or filtered_df.empty:
            return {
                'total_users': 0.0,
                'gender': {'male': 0.0, 'female': 0.0},
                'age': {f'age_{i}': 0.0 for i in range(1, 10)} | {'age_other': 0.0}
            }

        # Calculate weighted demographics
        weights = filtered_df[metric].values
        total_users = float(weights.sum())

        if total_users == 0:
            return {
                'total_users': 0.0,
                'gender': {'male': 0.0, 'female': 0.0},
                'age': {f'age_{i}': 0.0 for i in range(1, 10)} | {'age_other': 0.0}
            }

        # Weighted gender percentages
        male_pct = float((filtered_df['sex_1'] * weights).sum() / total_users)
        female_pct = float((filtered_df['sex_2'] * weights).sum() / total_users)

        # Weighted age percentages
        age_dist = {}
        for i in range(1, 10):
            col = f'age_{i}'
            if col in filtered_df.columns:
                age_dist[col] = float((filtered_df[col] * weights).sum() / total_users)

        if 'age_other' in filtered_df.columns:
            age_dist['age_other'] = float((filtered_df['age_other'] * weights).sum() / total_users)

        return {
            'total_users': total_users,
            'gender': {
                'male': male_pct,
                'female': female_pct
            },
            'age': age_dist
        }

    def get_metadata(self) -> Dict:
        """
        Get available months, hours, metrics, and day types.

        Returns:
            Dictionary with months, hours, metrics, day_types lists
        """
        return {
            'months': self.available_months,
            'hours': self.available_hours,
            'day_types': self.available_day_types,
            'metrics': [
                {'key': 'avg_total_users', 'label': '全部停留人數'},
                {'key': 'avg_users_under_10min', 'label': '停留10分鐘以下'},
                {'key': 'avg_users_10_30min', 'label': '停留10-30分鐘'},
                {'key': 'avg_users_over_30min', 'label': '停留30分鐘以上'}
            ],
            'total_locations': len(self.df),
            'data_coverage': {
                'total_data_points': len(self.df),
                'unique_locations': len(self.df.groupby(['gx', 'gy'])),
                'time_periods': len(self.lookup_dict)
            }
        }


# Global cache instance (initialized on app startup)
_data_cache: Optional[DataCache] = None


def initialize_cache(csv_path: str):
    """Initialize the global data cache."""
    global _data_cache
    _data_cache = DataCache(csv_path)
    logger.info("Data cache initialized successfully")


def get_cache() -> DataCache:
    """Get the global data cache instance."""
    if _data_cache is None:
        raise RuntimeError("Data cache not initialized. Call initialize_cache() first.")
    return _data_cache
