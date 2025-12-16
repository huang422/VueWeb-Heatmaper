#!/bin/bash

# Start Frontend Development Server
# Usage: ./start_frontend.sh

echo "======================================"
echo "Starting Frontend Development Server..."
echo "======================================"

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠ node_modules not found. Installing dependencies..."
    npm install
fi

# Start the dev server
echo ""
echo "Starting Vite dev server on http://localhost:5173"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

npm run dev
