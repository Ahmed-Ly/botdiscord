@echo off
title Discord Bot Auto Setup
color 0A

set REPO_URL=https://github.com/Ahmed-Ly/botdiscord.git
set REPO_DIR=botdiscord
set VENV_DIR=eee

echo.
echo ================================================
echo        Discord Bot Auto Setup Script
echo ================================================
echo.

:: ============================================
:: Step 1: Check Internet Connection
:: ============================================
echo Checking Internet connection...
ping github.com -n 1 >nul
if errorlevel 1 (
    color 0C
    echo [ERROR] No internet connection. Please check your connection.
    pause
    exit /b
) else (
    color 0A
    echo [OK] Internet connection is active.
)

:: ============================================
:: Step 2: Check Python Installation
:: ============================================
echo.
echo Checking if Python is installed...
where python >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Python is not installed. Please install Python first.
    pause
    exit /b
) else (
    color 0A
    echo [OK] Python is installed successfully.
)

:: ============================================
:: Step 3: Check Git Installation
:: ============================================
echo.
echo Checking if Git is installed...
where git >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Git is not installed. Please install Git first.
    pause
    exit /b
) else (
    color 0A
    echo [OK] Git is installed successfully.
)

:: ============================================
:: Step 4: Clone the Repository
:: ============================================
echo.
echo Cloning repository...
if exist "%REPO_DIR%" (
    color 0E
    echo [INFO] Repository folder "%REPO_DIR%" already exists. Skipping clone.
) else (
    git clone %REPO_URL%
    if errorlevel 1 (
        color 0C
        echo [ERROR] Failed to clone repository.
        pause
        exit /b
    ) else (
        color 0A
        echo [OK] Repository cloned successfully.
    )
)

:: ============================================
:: Step 5: Create Python Virtual Environment
:: ============================================
echo.
echo Creating Python virtual environment...
python -m venv %VENV_DIR%
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b
) else (
    color 0A
    echo [OK] Virtual environment created successfully.
)

:: ============================================
:: Step 6: Copy Project Files
:: ============================================
echo.
echo Copying project files to virtual environment's Scripts folder...
xcopy /E /I /Y "%REPO_DIR%\*" "%VENV_DIR%\Scripts\" >nul
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to copy project files.
    pause
    exit /b
) else (
    color 0A
    echo [OK] Project files copied successfully.
)

:: ============================================
:: Step 7: Activate Virtual Environment
:: ============================================
echo.
echo Changing directory to Scripts folder...
cd %VENV_DIR%\Scripts

echo.
echo Activating virtual environment...
call activate.bat

:: ============================================
:: Step 8: Install Required Python Packages
:: ============================================
echo.
echo Installing required Python packages...
pip install discord.py Flask requests configparser
if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to install packages.
    pause
    exit /b
) else (
    color 0A
    echo [OK] Packages installed successfully.
)

:: ============================================
:: Step 9: User Configuration Input
:: ============================================
echo.
color 0E
echo ================================================
echo Please enter the following configuration details:
echo ================================================
echo.

set /p username="Username: "
set /p password="Password: "
set /p host="Host: "
set /p port="Port: "
set /p resource="Resource: "
set /p bottoken="Bot Token: "
set /p channel="Channel: "

:: ============================================
:: Step 10: Write config.ini File
:: ============================================
echo.
echo Writing configuration to config.ini...
(
    echo [MTA]
    echo username=%username%
    echo password=%password%
    echo host=%host%
    echo port=%port%
    echo resource=%resource%
    echo bottoken=%bottoken%
    echo channel=%channel%
) > config.ini

if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to write config.ini.
    pause
    exit /b
) else (
    color 0A
    echo [OK] The configuration file has been updated successfully.
)

:: ============================================
:: Step 11: Run Python Script
:: ============================================
echo.
color 0E
echo ================================================
echo Running Python script...
echo ================================================

if exist scr.py (
    color 0A
    python scr.py
) else (
    color 0C
    echo [ERROR] scr.py not found!
)

:: ============================================
:: End of Script
:: ============================================
echo.
color 07
echo ================================================
echo Script execution completed.
echo ================================================
pause
