@echo off
set REPO_URL=https://github.com/Ahmed-Ly/botdiscord.git
set REPO_DIR=botdiscord
set VENV_DIR=eee

echo Cloning repository...
if exist "%REPO_DIR%" (
    echo Repository folder "%REPO_DIR%" already exists. Skipping clone.
) else (
    git clone %REPO_URL%
)

echo Creating Python virtual environment...
python -m venv %VENV_DIR%

echo Copying project files to virtual environment's Scripts folder...
xcopy /E /I /Y "%REPO_DIR%\*" "%VENV_DIR%\Scripts\"

echo Changing directory to the Scripts folder...
cd %VENV_DIR%\Scripts

echo Activating virtual environment...
call activate.bat

echo Installing required Python packages...
pip install discord.py Flask requests configparser


@echo off
echo Please enter the following configuration details:
echo.

set /p username="Username: "
set /p password="Password: "
set /p host="Host: "
set /p port="Port: "
set /p resource="Resource: "
set /p bottoken="Bot Token: "
set /p channel="Channel: "

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

echo.

echo The configuration file has been updated successfully.

echo Running Python script...
if exist scr.py (
    python scr.py
) else (
    echo scr.py not found!
)



pause
