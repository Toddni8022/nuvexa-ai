@echo off
echo ================================================
echo Misinformation Debunking Copilot - Setup
echo ================================================
echo.

cd /d "%~dp0"

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)
echo.

echo Step 2: Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
)
echo.

echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 4: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 5: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo Step 6: Installing Playwright browsers...
playwright install chromium
if errorlevel 1 (
    echo ERROR: Failed to install Playwright browsers!
    pause
    exit /b 1
)
echo.

echo Step 7: Setting up configuration...
if not exist ".env" (
    copy .env.example .env
    echo Created .env file. Please edit it with your settings.
) else (
    echo .env file already exists.
)
echo.

echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file if needed (default is mock mode - no API key needed)
echo 2. Edit data\targets.json with your Facebook targets
echo 3. Run START_DASHBOARD.bat to launch the application
echo.
echo For more information, see README.md
echo.
pause
