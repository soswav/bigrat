@echo off

:: colors for text, needed for actually reading the text lol
set RED=^[[0;31m
set GREEN=^[[0;32m
set NC=^[[0m

cls & echo. & echo.

set /p choice="do you have python & pip already installed? (y/n) "
if /i "%choice%"=="y" (
    echo %GREEN%alrighty!%NC%
) else (
    echo %GREEN%installing python and pip with pacman...%NC%
    pacman -S python python-pip || (echo %RED%didn't work, trying dnf...%NC% & timeout 2 & dnf install python python-pip || (echo %RED%didn't work, trying apt...%NC% & timeout 2 & apt install python3 python3-pip))
)

cls & echo. & echo.
echo %GREEN%i would like to mention that you need to toggle some stuff on discord.com/developers before continuing%NC%
echo %GREEN%go to your bot, then search for 'Privileged Gateway Intents' on the bot tab, toggle everything you see there%NC%
echo %RED%i'm going to make you wait 10 seconds, to make sure you read all this, sorry!%NC%
timeout 10

timeout 2 & cls & echo. & echo.
cd C:\Users\%USERNAME%\bigrat & echo %RED%folder exists, deleting with sudo%NC% & rmdir /s /q C:\Users\%USERNAME%\bigrat\ & timeout 2 & cd C:\Users\%USERNAME%\
echo %GREEN%cloning git repo...%NC%
git clone https://github.com/soswav/bigrat.git || (echo %RED%no git? trying to install with pacman...%NC% & timeout 2 & pacman -S git & echo %GREEN%installed! retrying...%NC% & timeout 2 & git clone https://github.com/soswav/bigrat.git) || (echo %RED%didn't work, trying dnf...%NC% & timeout 2 & dnf install git & echo %GREEN%installed! retrying...%NC% & timeout 2 & git clone https://github.com/soswav/bigrat.git) || (echo %RED%didn't work, trying apt...%NC% & timeout 2 & apt install git & echo %GREEN%installed! retrying...%NC% & timeout 2 & git clone https://github.com/soswav/bigrat.git)

echo %GREEN%generating venv with python, please wait!%NC%
python -m venv C:\Users\%USERNAME%\bigrat\bot\.venv & call C:\Users\%USERNAME%\bigrat\bot\.venv\Scripts\activate.bat
