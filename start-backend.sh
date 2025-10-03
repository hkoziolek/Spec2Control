#!/bin/bash
# Spec2Control Backend API Startup Script
# Starts the FastAPI backend server with uvicorn

cd "$(dirname "$0")/src"

echo "================================="
echo "Spec2Control Backend API"
echo "================================="
echo "Server will run on http://127.0.0.1:8001"
echo "Press Ctrl+C to stop"
echo "================================="
echo ""

# Start with uvicorn directly for better control
# Note: Using python -m uvicorn for proper module loading
python -m uvicorn spec2control_backend:app --host 127.0.0.1 --port 8001 --reload
