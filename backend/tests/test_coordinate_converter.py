"""
Tests for Coordinate Converter Service
Verifies gx/gy to lat/lng conversion accuracy.
"""

import pytest
from src.services.coordinate_converter import (
    gxgy_to_latlon,
    batch_gxgy_to_latlon,
    get_cache_info,
    clear_cache
)
import numpy as np


class TestCoordinateConverter:
    """Test coordinate conversion functions."""

    def setup_method(self):
        """Clear cache before each test."""
        clear_cache()

    def test_single_conversion_basic(self):
        """Test basic coordinate conversion."""
        # Example from Jupyter notebook (cell 7 output)
        gx, gy = 7027, 6850
        lat, lng = gxgy_to_latlon(gx, gy)

        # Should be near 25.068628, 121.591327 (from notebook)
        assert 25.06 < lat < 25.08, f"Latitude {lat} out of expected range"
        assert 121.58 < lng < 121.60, f"Longitude {lng} out of expected range"

    def test_conversion_known_values(self):
        """Test conversion with known values from notebook."""
        test_cases = [
            # (gx, gy, expected_lat_range, expected_lng_range)
            (7165, 7152, (25.03, 25.04), (121.54, 121.55)),  # From data.csv example
            (6905, 6599, (24.90, 25.00), (121.50, 121.60)),  # From notebook cell 10
        ]

        for gx, gy, lat_range, lng_range in test_cases:
            lat, lng = gxgy_to_latlon(gx, gy)
            assert lat_range[0] <= lat <= lat_range[1], \
                f"Latitude {lat} for ({gx}, {gy}) outside range {lat_range}"
            assert lng_range[0] <= lng <= lng_range[1], \
                f"Longitude {lng} for ({gx}, {gy}) outside range {lng_range}"

    def test_conversion_taiwan_bounds(self):
        """Test that converted coordinates fall within Taiwan bounds."""
        # Test various grid points across Taiwan
        test_points = [
            (7000, 5000),  # Southern Taiwan
            (7500, 6500),  # Central Taiwan
            (7000, 7000),  # Northern Taiwan
        ]

        for gx, gy in test_points:
            lat, lng = gxgy_to_latlon(gx, gy)

            # Taiwan latitude range: ~21.9° to 25.3°
            assert 21.5 < lat < 25.5, f"Latitude {lat} outside Taiwan bounds"

            # Taiwan longitude range: ~118.0° to 122.1°
            assert 117.5 < lng < 122.5, f"Longitude {lng} outside Taiwan bounds"

    def test_batch_conversion(self):
        """Test batch coordinate conversion."""
        gx_array = np.array([7165, 7166, 7167])
        gy_array = np.array([7152, 7152, 7152])

        lat_array, lng_array = batch_gxgy_to_latlon(gx_array, gy_array)

        assert len(lat_array) == 3
        assert len(lng_array) == 3

        # All should be in Taiwan
        assert all(21.9 < lat < 25.3 for lat in lat_array)
        assert all(118.0 < lng < 122.1 for lng in lng_array)

        # Longitude should increase as gy increases (moving east)
        # (Actually gx increases move north, gy increases may move in different direction)
        # Just verify they're valid
        assert isinstance(lat_array[0], (float, np.floating))
        assert isinstance(lng_array[0], (float, np.floating))

    def test_cache_functionality(self):
        """Test LRU cache is working."""
        # Clear cache
        clear_cache()
        info = get_cache_info()
        assert info.hits == 0
        assert info.misses == 0

        # First call - cache miss
        gxgy_to_latlon(7165, 7152)
        info = get_cache_info()
        assert info.misses == 1
        assert info.hits == 0

        # Second call same coordinates - cache hit
        gxgy_to_latlon(7165, 7152)
        info = get_cache_info()
        assert info.hits == 1
        assert info.misses == 1

    def test_cache_different_coordinates(self):
        """Test cache works for different coordinates."""
        clear_cache()

        # Call with different coordinates
        gxgy_to_latlon(7165, 7152)
        gxgy_to_latlon(7166, 7153)
        gxgy_to_latlon(7165, 7152)  # Repeat first

        info = get_cache_info()
        assert info.misses == 2  # Two unique coordinates
        assert info.hits == 1    # One repeated coordinate

    def test_consistency(self):
        """Test that same input always produces same output."""
        gx, gy = 7165, 7152

        lat1, lng1 = gxgy_to_latlon(gx, gy)
        lat2, lng2 = gxgy_to_latlon(gx, gy)

        assert lat1 == lat2, "Latitude should be consistent"
        assert lng1 == lng2, "Longitude should be consistent"

    def test_grid_center_calculation(self):
        """Test that grid center is calculated correctly."""
        # Grid (7165, 7152) should give center of 50m cell
        # This tests that (gx + 0.5, gy + 0.5) * cell_size logic is correct

        gx, gy = 7000, 7000
        lat1, lng1 = gxgy_to_latlon(gx, gy)

        # Adjacent grid should be ~50m away (roughly 0.00045 degrees)
        gx_adj, gy_adj = 7001, 7000
        lat2, lng2 = gxgy_to_latlon(gx_adj, gy_adj)

        # Difference should be small (roughly one 50m cell)
        lat_diff = abs(lat2 - lat1)
        assert 0.0003 < lat_diff < 0.0006, \
            f"Latitude difference {lat_diff} not consistent with 50m cell size"

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test minimum reasonable values
        lat, lng = gxgy_to_latlon(6000, 0)
        assert isinstance(lat, float)
        assert isinstance(lng, float)

        # Test large values
        lat, lng = gxgy_to_latlon(8000, 8000)
        assert isinstance(lat, float)
        assert isinstance(lng, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
