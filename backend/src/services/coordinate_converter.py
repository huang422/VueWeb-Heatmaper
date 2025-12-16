"""
Coordinate Conversion Service
Converts between Taiwan TWD97 TM2 grid coordinates (gx, gy) and WGS84 latitude/longitude.

Based on the inverse transformation formulas from data/gxgy_transfer.ipynb.
Uses Numba JIT compilation for performance (~260,000 conversions/second).
"""

import math
from functools import lru_cache
from typing import Tuple
from numba import jit
import numpy as np


# TWD97 TM2 Parameters
A = 6378137  # WGS84 ellipsoid semi-major axis (meters)
F = 1 / 298.257222101  # Flattening
K = 0.9999  # Scale factor
CLNG = 121.0  # Central meridian (degrees)
FALSE_EASTING = 250000  # False easting (meters)
E2 = 2 * F - F * F  # Eccentricity squared

# Grid parameters
GRID_SW_LAT_OFFSET = -32871.4054  # Southwest corner latitude offset (meters)
GRID_SW_LNG_OFFSET = 2422126.0017  # Southwest corner longitude offset (meters)
GRID_CELL_SIZE = 50  # Grid cell size (meters)


@jit(nopython=True)
def _tm2_to_latlon_jit(x: float, y: float) -> Tuple[float, float]:
    """
    Convert TM2 coordinates to lat/lon using Numba JIT compilation.

    Uses iterative binary search to find footpoint latitude.
    Converges when |Z - yb| < 0.001 meters (typically ~20 iterations).

    Args:
        x: TM2 X coordinate (meters, easting)
        y: TM2 Y coordinate (meters, northing)

    Returns:
        Tuple of (latitude, longitude) in decimal degrees
    """
    a = A
    f = F
    k = K
    clng = CLNG
    false_easting = FALSE_EASTING
    e2 = E2

    xb = (x - false_easting) / k
    yb = y / k

    # Binary search for footpoint latitude
    F1 = -89.999
    F2 = 89.999

    for _ in range(1000):
        c1 = 0.5 * (F1 + F2)
        C = c1 / 180 * math.pi

        # Calculate Z using meridian arc formula
        Z = a * (
            (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256) * C
            - (3 * e2 / 8 + 3 * e2 * e2 / 32 + 45 * e2 * e2 * e2 / 1024) * math.sin(2 * C)
            + (15 * e2 * e2 / 256 + 45 * e2 * e2 * e2 / 1024) * math.sin(4 * C)
            - (35 * e2 * e2 * e2 / 3072) * math.sin(6 * C)
        )

        DZY = Z - yb

        # Convergence check
        if DZY > 0:
            if DZY < 0.001:
                break
            F2 = c1
        else:
            if DZY > -0.001:
                break
            F1 = c1

    # Calculate final lat/lon
    slat = C
    lS = math.sin(slat)
    lT = math.tan(slat)
    lSec = 1 / math.cos(slat)

    R = a * (1 - e2) / math.pow(1 - e2 * lS * lS, 1.5)
    N = a / math.sqrt(1 - e2 * lS * lS)

    lat = slat - (xb * xb * lT) / (2 * R * N) + \
          math.pow(xb, 4) / (24 * R * N * N * N) * (5 + 3 * lT * lT) * lT

    lng = xb * lSec / N - \
          xb * xb * xb / (6 * N * N * N) * lSec * (N / R + 2 * lT * lT) + \
          math.pow(xb, 5) / (120 * math.pow(N, 5)) * lSec * (5 + 28 * lT * lT + 24 * math.pow(lT, 4))

    lat = lat / math.pi * 180
    lng = lng / math.pi * 180
    lng += clng

    return (lat, lng)


@lru_cache(maxsize=10000)
def gxgy_to_latlon(gx: int, gy: int) -> Tuple[float, float]:
    """
    Convert grid coordinates (gx, gy) to WGS84 latitude/longitude.

    Uses LRU caching for frequently accessed coordinates.
    Grid center is calculated as (gx + 0.5, gy + 0.5) * GRID_CELL_SIZE.

    Args:
        gx: Grid X coordinate (integer index)
        gy: Grid Y coordinate (integer index)

    Returns:
        Tuple of (latitude, longitude) in decimal degrees

    Example:
        >>> lat, lon = gxgy_to_latlon(7165, 7152)
        >>> print(f"Lat: {lat:.6f}, Lon: {lon:.6f}")
        Lat: 25.033311, Lon: 121.543653
    """
    # Calculate TM2 coordinates for grid center
    tm2_x = GRID_SW_LAT_OFFSET + (gx + 0.5) * GRID_CELL_SIZE
    tm2_y = GRID_SW_LNG_OFFSET + (gy + 0.5) * GRID_CELL_SIZE

    return _tm2_to_latlon_jit(tm2_x, tm2_y)


def batch_gxgy_to_latlon(gx_array: np.ndarray, gy_array: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert batch of grid coordinates to lat/lon.

    Optimized for vectorized operations on large datasets.

    Args:
        gx_array: NumPy array of grid X coordinates
        gy_array: NumPy array of grid Y coordinates

    Returns:
        Tuple of (latitude_array, longitude_array) as NumPy arrays
    """
    # Calculate TM2 coordinates for grid centers
    # gx corresponds to X (easting/longitude), gy corresponds to Y (northing/latitude)
    tm2_x_array = GRID_SW_LNG_OFFSET + (gx_array + 0.5) * GRID_CELL_SIZE
    tm2_y_array = GRID_SW_LAT_OFFSET + (gy_array + 0.5) * GRID_CELL_SIZE

    # Convert using JIT-compiled function
    results = np.array([
        _tm2_to_latlon_jit(x, y)
        for x, y in zip(tm2_x_array, tm2_y_array)
    ])

    return results[:, 0], results[:, 1]


# Cache statistics for monitoring
def get_cache_info():
    """
    Get LRU cache statistics for monitoring performance.

    Returns:
        CacheInfo object with hits, misses, maxsize, currsize
    """
    return gxgy_to_latlon.cache_info()


def clear_cache():
    """Clear the LRU cache (useful for testing or memory management)."""
    gxgy_to_latlon.cache_clear()
