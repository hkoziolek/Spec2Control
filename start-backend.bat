@echo off
REM Spec2Control Backend API Startup Script
REM Starts the FastAPI backend server with uvicorn

cd /d "%~dp0src"

echo =================================
echo Spec2Control Backend API
echo =================================
echo Server will run on http://127.0.0.1:8001
echo Press Ctrl+C to stop
echo =================================
echo.

REM Start with uvicorn directly for better control
REM Note: Using python -m uvicorn for proper module loading
python -m uvicorn spec2control_backend:app --host 127.0.0.1 --port 8001 --reload
