@echo off
title NUVEXA AI
color 0B
cls
echo.
echo  ========================================
echo         NUVEXA AI Assistant
echo         Your Living AI with Execution Power
echo  ========================================
echo.
echo  Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found!
    echo  Please run SETUP.bat first or install Python.
    echo.
    pause
    exit /b 1
)
echo.
echo  Starting NUVEXA...
echo  The app will open in your browser shortly.
echo.
echo  Press Ctrl+C to stop the application.
echo  ========================================
echo.
python -m streamlit run app.py
if errorlevel 1 (
    echo.
    echo  ERROR: Failed to start NUVEXA!
    echo  Make sure you've run SETUP.bat and added your API key to .env
    echo.
    pause
    exit /b 1
)
