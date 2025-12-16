#!/usr/bin/env python3
"""
Quick test script to verify backend imports and basic functionality
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_path))

def test_imports():
    """Test that all modules can be imported"""
    try:
        print("Testing imports...")

        # Test coordinate converter
        from src.services.coordinate_converter import gxgy_to_latlon
        print("✓ coordinate_converter imported")

        # Test a conversion
        lat, lng = gxgy_to_latlon(7165, 7152)
        print(f"✓ Coordinate conversion works: ({7165}, {7152}) -> ({lat:.6f}, {lng:.6f})")

        # Verify it's in Taiwan bounds
        assert 21.9 < lat < 25.3, "Latitude out of Taiwan bounds"
        assert 118.0 < lng < 122.1, "Longitude out of Taiwan bounds"
        print("✓ Coordinates are within Taiwan bounds")

        # Test data loader
        from src.services.data_loader import DataCache
        print("✓ data_loader imported")

        # Test config
        from src.utils.config import DATA_PATH, VALID_MONTHS
        print(f"✓ config imported, DATA_PATH: {DATA_PATH}")
        print(f"✓ Valid months: {VALID_MONTHS}")

        # Test models
        from src.models.location_data import LocationPoint
        print("✓ location_data models imported")

        # Test API models
        from src.api.models.response import HeatmapResponse
        from src.api.models.request import HeatmapRequest
        print("✓ API models imported")

        print("\n✅ All imports successful!")
        return True

    except Exception as e:
        print(f"\n❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_loading():
    """Test data loading functionality"""
    try:
        print("\n" + "="*50)
        print("Testing data loading...")

        from src.services.data_loader import DataCache
        from src.utils.config import get_data_path

        data_path = get_data_path()
        print(f"✓ Data path: {data_path}")

        cache = DataCache(str(data_path))
        print(f"✓ DataCache initialized")
        print(f"✓ Available months: {cache.available_months}")
        print(f"✓ Available hours: {len(cache.available_hours)} hours (0-23)")
        print(f"✓ Total data points: {len(cache.df)}")

        # Test heatmap data retrieval
        heatmap_data = cache.get_heatmap_data(202412, 0, 'avg_total_users')
        print(f"✓ Retrieved {len(heatmap_data)} data points for month=202412, hour=0")

        if heatmap_data:
            first_point = heatmap_data[0]
            print(f"✓ Sample data point: gx={first_point['gx']}, gy={first_point['gy']}, "
                  f"lat={first_point['lat']:.6f}, lng={first_point['lng']:.6f}, "
                  f"weight={first_point['weight']:.2f}")

        # Test demographics
        demo_data = cache.get_demographics(202412, 0, 'avg_total_users')
        print(f"✓ Demographics retrieved, total_users={demo_data['total_users']:.2f}")
        print(f"✓ Gender distribution: Male={demo_data['gender']['male']:.2f}%, "
              f"Female={demo_data['gender']['female']:.2f}%")

        # Test metadata
        metadata = cache.get_metadata()
        print(f"✓ Metadata retrieved: {metadata['total_locations']} total locations")

        print("\n✅ Data loading tests successful!")
        return True

    except Exception as e:
        print(f"\n❌ Data loading test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("Backend Integration Test")
    print("=" * 50)

    success = True
    success = test_imports() and success
    success = test_data_loading() and success

    if success:
        print("\n" + "="*50)
        print("🎉 All tests passed!")
        print("="*50)
        sys.exit(0)
    else:
        print("\n" + "="*50)
        print("❌ Some tests failed")
        print("="*50)
        sys.exit(1)
