@echo off
SETLOCAL
SET VENV_DIR=venv
SET PYTHON=%VENV_DIR%\Scripts\python.exe
SET PIP=%VENV_DIR%\Scripts\pip.exe
SET REQUIREMENTS=requirements.txt

:: Check if Python is installed
where python >nul 2>nul
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python 3.x and try again.
    pause
    exit /b 1
)

:: Create virtual environment
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
    IF ERRORLEVEL 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists. Skipping creation.
)

:: Install required libraries
echo Installing required libraries...
%PIP% install -r %REQUIREMENTS%
IF ERRORLEVEL 1 (
    echo Failed to install required libraries.
    pause
    exit /b 1
)

:: Run setup.py
echo Running setup.py...
%PYTHON% setup.py
IF ERRORLEVEL 1 (
    echo An error occurred while running setup.py.
    pause
    exit /b 1
)

:: Run the GUI application
echo Starting the GUI application...
%PYTHON% src/gui/run_app.py
IF ERRORLEVEL 1 (
    echo Failed to start the GUI application.
    pause
    exit /b 1
)

pause
