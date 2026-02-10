@echo off
REM Windows batch script to test API with samples

echo ====================================
echo   LLM Observability Sample Tester
echo ====================================
echo.

REM Check if API is running
echo Checking if API is running...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: API is not running!
    echo.
    echo Please start the API first:
    echo   python run_phase5.py
    echo.
    pause
    exit /b 1
)

echo API is running!
echo.

REM Run the test script
echo Running sample tests...
echo.
python test_samples.py

echo.
echo ====================================
echo   Testing Complete!
echo ====================================
echo.
pause
