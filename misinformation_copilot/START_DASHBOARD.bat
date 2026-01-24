@echo off
echo Starting Misinformation Debunking Copilot Dashboard...
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run SETUP.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
streamlit run app/ui.py

pause
