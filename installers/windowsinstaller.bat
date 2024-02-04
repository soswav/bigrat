@echo off
set "python_version=3.10.0"
set "url=https://www.python.org/ftp/python/%python_version%/python-%python_version%-amd64.exe"
set "installer=python-%python_version%-amd64.exe"
set "targetdir=C:\Python%python_version%"

echo Downloading Python installer...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%url%', '%installer%')"

echo Installing Python...
start /wait %installer% /quiet /passive TargetDir=%targetdir% Include_test=0

echo Adding Python to the system's PATH variable...
setx path "%path%;%targetdir%" /M

echo Installation of Python complete.

set "git_version=2.43.0"
set "git_url=https://github.com/git-for-windows/git/releases/download/v%git_version%.windows.1/Git-%git_version%-64-bit.exe"
set "git_installer=Git-%git_version%-64-bit.exe"

echo Downloading Git installer...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%git_url%', '%git_installer%')"

echo Installing Git...
start /wait %git_installer% /SP- /VERYSILENT /NORESTART /NOCANCEL /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"

echo Adding Git to the system's PATH variable...
setx path "%path%;C:\Program Files\Git\cmd" /M

echo Installation of Git complete.

echo Open git CMD and do git clone https://github.com/soswav/bigrat
echo Download requirments by doing:
echo pip install discord.py pyyaml requests asyncio
pause
