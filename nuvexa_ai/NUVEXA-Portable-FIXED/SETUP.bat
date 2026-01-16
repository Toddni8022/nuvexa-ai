@echo off
title NUVEXA AI - Setup
color 0A
echo.
echo  ========================================
echo         NUVEXA AI - Setup Wizard
echo  ========================================
echo.
echo  Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found!
    echo  Please install Python from: https://www.python.org/downloads/
    echo.
    pause
    exit
)
echo  Python found!
echo.
echo  Installing dependencies...
pip install -r requirements.txt
echo.
echo  ========================================
echo  Setup Complete!
echo  ========================================
echo.
echo  IMPORTANT: Edit .env file and add your OpenAI API key
echo  Then run RUN_NUVEXA.bat
echo.
pause
