"""
Build Script for Windows Executable - Optimized for Minimal Size
Creates a lightweight standalone .exe with only essential runtime files
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Project paths
BACKEND_DIR = Path(__file__).parent
PROJECT_ROOT = BACKEND_DIR.parent
DATA_DIR = PROJECT_ROOT / 'data'
DIST_DIR = BACKEND_DIR / 'dist'
BUILD_DIR = BACKEND_DIR / 'build'

def check_prerequisites():
    """Check if all required files and dependencies are present"""
    print("🔍 Checking prerequisites...")

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False

    # Check if data file exists
    data_file = DATA_DIR / 'data.csv'
    if not data_file.exists():
        print(f"❌ Data file not found at {data_file}")
        return False
    print(f"✓ Data file found: {data_file}")

    return True

def clean_build_dirs():
    """Remove old build artifacts"""
    print("\n🧹 Cleaning old build artifacts...")

    for dir_path in [DIST_DIR, BUILD_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"✓ Removed {dir_path}")

def build_executable():
    """Run PyInstaller to build the executable"""
    print("\n🔨 Building lightweight executable with PyInstaller...")

    # PyInstaller arguments - optimized for minimal size
    args = [
        'pyinstaller',
        '--name=StoreHeatmap',
        '--onefile',  # Single executable file
        '--console',  # Keep console for debugging (change to --windowed for production)

        # Add only essential data files
        f'--add-data={DATA_DIR / "data.csv"}{os.pathsep}data',

        # Hidden imports (only essential modules)
        '--hidden-import=uvicorn.logging',
        '--hidden-import=uvicorn.loops',
        '--hidden-import=uvicorn.loops.auto',
        '--hidden-import=uvicorn.protocols',
        '--hidden-import=uvicorn.protocols.http',
        '--hidden-import=uvicorn.protocols.http.auto',
        '--hidden-import=uvicorn.protocols.websockets',
        '--hidden-import=uvicorn.protocols.websockets.auto',
        '--hidden-import=uvicorn.lifespan',
        '--hidden-import=uvicorn.lifespan.on',
        '--hidden-import=numba',
        '--hidden-import=numba.core',
        '--hidden-import=numba.core.typing',

        # Exclude ALL unnecessary modules to minimize size
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
        '--exclude-module=IPython',
        '--exclude-module=notebook',
        '--exclude-module=jupyter',
        '--exclude-module=pytest',
        '--exclude-module=sphinx',
        '--exclude-module=setuptools',
        '--exclude-module=pip',
        '--exclude-module=wheel',
        '--exclude-module=PIL',
        '--exclude-module=PIL.Image',
        '--exclude-module=PyQt5',
        '--exclude-module=PyQt6',
        '--exclude-module=PySide2',
        '--exclude-module=PySide6',
        '--exclude-module=wx',

        # Exclude testing modules
        '--exclude-module=unittest',
        '--exclude-module=test',
        '--exclude-module=tests',
        '--exclude-module=doctest',

        # Exclude documentation modules
        '--exclude-module=pydoc',
        '--exclude-module=pydoc_data',

        # Strip debug symbols and optimize
        '--strip',  # Strip symbols from binary (Linux/Mac)
        '--noupx',  # Disable UPX compression (can cause issues)

        # Optimize imports
        '--optimize=2',  # Highest Python optimization level

        # Exclude unnecessary binary files
        '--exclude-module=_tkinter',
        '--exclude-module=curses',
        '--exclude-module=readline',

        # Clean build
        '--clean',
        '--noconfirm',

        # Logging
        '--log-level=WARN',

        # Entry point
        str(BACKEND_DIR / 'src' / 'main.py')
    ]

    # Run PyInstaller
    try:
        result = subprocess.run(args, check=True, cwd=BACKEND_DIR)
        print("\n✅ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error code {e.returncode}")
        return False

def optimize_build():
    """Post-build optimization to reduce size further"""
    print("\n⚡ Optimizing build output...")

    # Remove spec file if not needed
    spec_file = BACKEND_DIR / 'StoreHeatmap.spec'
    if spec_file.exists():
        spec_file.unlink()
        print("✓ Removed .spec file")

    # Remove build directory (not needed after build)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print("✓ Removed build directory")

def verify_build():
    """Verify the built executable exists"""
    print("\n🔍 Verifying build output...")

    exe_path = DIST_DIR / 'StoreHeatmap.exe'
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ Executable created: {exe_path}")
        print(f"✓ Size: {size_mb:.2f} MB")

        # Size warnings
        if size_mb > 100:
            print("⚠️  Warning: Executable is large. Consider reviewing dependencies.")
        elif size_mb < 50:
            print("✅ Excellent: Executable is lightweight!")

        return True
    else:
        print(f"❌ Executable not found at {exe_path}")
        return False

def print_instructions():
    """Print usage instructions"""
    print("\n📝 Build Complete!")
    print("\n" + "=" * 60)
    print("The executable is ready to use:")
    print(f"  Location: {DIST_DIR / 'StoreHeatmap.exe'}")
    print("\nWhat's included:")
    print("  ✓ Backend API server (FastAPI + Uvicorn)")
    print("  ✓ Data processing (Pandas + NumPy + Numba)")
    print("  ✓ Coordinate conversion (TWD97 TM2)")
    print("  ✓ Data file (data.csv)")
    print("\nWhat's excluded (to minimize size):")
    print("  ✗ Frontend files (serve separately or use CDN)")
    print("  ✗ Documentation and README files")
    print("  ✗ Test files and notebooks")
    print("  ✗ Development dependencies")
    print("\nTo run the application:")
    print("  1. Double-click StoreHeatmap.exe")
    print("  2. API server starts on http://localhost:8001")
    print("  3. Use frontend separately or via browser")
    print("\nTo distribute:")
    print("  - Copy StoreHeatmap.exe to target machine")
    print("  - Ensure data.csv is in the same directory")
    print("  - No installation or dependencies required")
    print("=" * 60)

def main():
    """Main build process"""
    print("=" * 60)
    print("Store Heatmap - Lightweight Windows Executable Builder")
    print("=" * 60)

    # Step 1: Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed. Please fix the issues above.")
        return 1

    # Step 2: Clean old builds
    clean_build_dirs()

    # Step 3: Build executable
    if not build_executable():
        print("\n❌ Build process failed.")
        return 1

    # Step 4: Optimize build
    optimize_build()

    # Step 5: Verify build
    if not verify_build():
        print("\n❌ Build verification failed.")
        return 1

    # Step 6: Print instructions
    print_instructions()

    return 0

if __name__ == '__main__':
    sys.exit(main())
