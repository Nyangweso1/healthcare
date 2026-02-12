@echo off
REM Healthcare Insurance Risk Prediction System - Startup Script
REM Created: January 3, 2026

echo.
echo ===============================================
echo Healthcare Insurance Risk Prediction System
echo ===============================================
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Failed to activate virtual environment
        pause
        exit /b 1
    )
)

echo [1/4] Checking data...
if not exist "data\healthcare_clean.csv" (
    echo WARNING: Cleaned data not found. Running preprocessing...
    python data_preprocessing.py
    if errorlevel 1 (
        echo ERROR: Data preprocessing failed!
        pause
        exit /b 1
    )
) else (
    echo ✓ Data found
)

echo.
echo [2/4] Checking model...
if not exist "models\insurance_risk_model.pkl" (
    echo WARNING: Model not found. Running training...
    python model_training.py
    if errorlevel 1 (
        echo ERROR: Model training failed!
        pause
        exit /b 1
    )
) else (
    echo ✓ Model found
)

echo.
echo [3/4] Initializing database...
python -c "from app import init_db; init_db(); print('Database ready')"
echo.

echo [4/4] Starting Flask application...
echo.
echo ===============================================
echo   Application URL: http://127.0.0.1:5000
echo   Press Ctrl+C to stop the server
echo ===============================================
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ERROR: Application crashed!
    echo Check the error messages above.
    pause
)
