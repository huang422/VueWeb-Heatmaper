"""
Build Script for Windows Executable
Automates PyInstaller execution to create standalone .exe
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Project paths
BACKEND_DIR = Path(__file__).parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / 'frontend'
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

    # Check if frontend is built
    frontend_dist = FRONTEND_DIR / 'dist'
    if not frontend_dist.exists() or not list(frontend_dist.glob('*')):
        print("❌ Frontend not built. Run: cd frontend && npm run build")
        return False
    print(f"✓ Frontend dist found at {frontend_dist}")

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
    print("\n🔨 Building executable with PyInstaller...")

    # PyInstaller arguments
    args = [
        'pyinstaller',
        '--name=StoreHeatmap',
        '--onefile',  # Single executable file
        '--windowed',  # No console window (GUI app)
        '--icon=NONE',  # Add icon path if you have one

        # Add data files
        f'--add-data={FRONTEND_DIR / "dist"}{os.pathsep}frontend/dist',
        f'--add-data={DATA_DIR / "data.csv"}{os.pathsep}data',

        # Hidden imports (modules not automatically detected)
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

        # Exclude unnecessary modules to reduce size
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
        '--exclude-module=IPython',
        '--exclude-module=notebook',

        # Enable UPX compression if available
        '--upx-dir=.',  # UPX will be used if found in PATH

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

def verify_build():
    """Verify the built executable exists"""
    print("\n🔍 Verifying build output...")

    exe_path = DIST_DIR / 'StoreHeatmap.exe'
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✓ Executable created: {exe_path}")
        print(f"✓ Size: {size_mb:.2f} MB")
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
    print("\nTo run the application:")
    print("  1. Double-click StoreHeatmap.exe")
    print("  2. Browser will open automatically")
    print("  3. Navigate to http://localhost:8000")
    print("\nTo distribute:")
    print("  - Copy StoreHeatmap.exe to target machine")
    print("  - No installation required")
    print("  - No Python or dependencies needed")
    print("=" * 60)

def main():
    """Main build process"""
    print("=" * 60)
    print("Store Heatmap - Windows Executable Builder")
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

    # Step 4: Verify build
    if not verify_build():
        print("\n❌ Build verification failed.")
        return 1

    # Step 5: Print instructions
    print_instructions()

    return 0

if __name__ == '__main__':
    sys.exit(main())
