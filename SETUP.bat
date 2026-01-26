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
    echo  Please install Python 3.8+ from: https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
python --version
echo  Python found!
echo.
echo  Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo.
echo  Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo  ERROR: Failed to install dependencies!
    echo  Try running: python -m pip install --upgrade pip
    echo  Then run this setup again.
    echo.
    pause
    exit /b 1
)
echo.
echo  ========================================
echo  Setup Complete!
echo  ========================================
echo.
echo  IMPORTANT: Edit .env file and add your OpenAI API key
echo  Get your API key at: https://platform.openai.com/api-keys
echo.
echo  Then run RUN_NUVEXA.bat to start NUVEXA!
echo.
pause
