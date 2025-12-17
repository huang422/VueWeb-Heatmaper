#!/bin/bash
###############################################################################
# Prepare files for Windows packaging
# Run this script on Ubuntu to create a minimal packaging folder
###############################################################################

set -e

echo "======================================================================"
echo "Preparing Windows Packaging Files"
echo "======================================================================"
echo ""

# Target directory
PACK_DIR=~/store_heatmap_windows
PROJECT_DIR=/home/user/Desktop/Tom/store_heatmap

# Clean old packaging directory
if [ -d "$PACK_DIR" ]; then
    echo "Cleaning old packaging directory..."
    rm -rf "$PACK_DIR"
fi

# Create directory structure
echo "Creating directory structure..."
mkdir -p "$PACK_DIR/backend/src"
mkdir -p "$PACK_DIR/frontend/dist"
mkdir -p "$PACK_DIR/data"

# Copy backend
echo "Copying backend files..."
cp -r "$PROJECT_DIR/backend/src" "$PACK_DIR/backend/"
cp "$PROJECT_DIR/backend/requirements.txt" "$PACK_DIR/backend/"
cp "$PROJECT_DIR/backend/build_exe.py" "$PACK_DIR/backend/"
cp "$PROJECT_DIR/backend/run_app.py" "$PACK_DIR/backend/"

# Copy frontend/dist
echo "Copying frontend build files..."
if [ -d "$PROJECT_DIR/frontend/dist" ]; then
    cp -r "$PROJECT_DIR/frontend/dist"/* "$PACK_DIR/frontend/dist/"
else
    echo "Error: frontend/dist does not exist!"
    echo "Please run: cd frontend && npm run build"
    exit 1
fi

# Copy data
echo "Copying data files..."
cp "$PROJECT_DIR/data/data.csv" "$PACK_DIR/data/"

# Create README
cat > "$PACK_DIR/README.txt" << 'EOF'
Store Heatmap - Windows Packaging Files
========================================

This folder contains all files needed for Windows packaging.

Build Steps:
-----------

1. Install Python 3.10 or higher
   https://www.python.org/downloads/

2. Open PowerShell or CMD, navigate to backend directory:
   cd backend

3. Install dependencies:
   pip install -r requirements.txt
   pip install pyinstaller

4. Run packaging:
   python build_exe.py

5. After completion, the exe file will be at:
   backend\dist\StoreHeatmap.exe

EOF

# Display result
echo ""
echo "======================================================================"
echo "Preparation Complete!"
echo "======================================================================"
echo ""
echo "Packaging folder: $PACK_DIR"
echo ""
echo "Files included:"
du -sh "$PACK_DIR"
echo ""
tree -L 2 "$PACK_DIR" 2>/dev/null || find "$PACK_DIR" -maxdepth 2 -type d
echo ""
echo "Next steps:"
echo "1. Copy the entire store_heatmap_windows folder to a Windows computer"
echo "2. Navigate to the backend directory on Windows"
echo "3. Run: python build_exe.py"
echo ""
echo "======================================================================"
