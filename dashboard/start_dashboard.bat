@echo off
REM EvoTransformer Dashboard Startup Script (Windows)
REM This script sets up and starts the customer dashboard

echo ==========================================
echo   EvoTransformer Customer Dashboard
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully
echo.
echo ==========================================
echo Starting Dashboard Server...
echo ==========================================
echo.
echo Dashboard URL: http://localhost:5000
echo API Endpoints: http://localhost:5000/api/*
echo Health Check: http://localhost:5000/health
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the Flask application
python app.py

pause
