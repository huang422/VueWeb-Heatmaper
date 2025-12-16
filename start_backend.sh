#!/bin/bash

# Start Backend Server
# Usage: ./start_backend.sh

echo "======================================"
echo "Starting Backend API Server..."
echo "======================================"

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Navigate to backend directory
cd "$SCRIPT_DIR/backend"

# Check if fapi conda environment exists
if [ -f ~/anaconda3/envs/fapi/bin/python ]; then
    echo "✓ Using conda environment: fapi"
    PYTHON_CMD=~/anaconda3/envs/fapi/bin/python
else
    echo "⚠ Warning: fapi environment not found, using system python"
    PYTHON_CMD=python3
fi

# Start the server
echo ""
echo "Starting server on http://127.0.0.1:8000"
echo "API Documentation: http://127.0.0.1:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Run from backend directory
$PYTHON_CMD -m src.main
