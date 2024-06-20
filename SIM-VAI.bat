@echo off
REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)

REM Install packages listed below
echo Installing Python packages...
pip install  -r requirements.txt
streamlit run Home.py