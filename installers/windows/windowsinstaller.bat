@echo off
cls

set title=wawas's installer of the modules!


REM Set the title of the console window
title %title%


echo Installing requirements...
pip install discord.py
pip install requests
pip install PyYAML

if %errorlevel% equ 0 (

    REM The command was successful
    echo Done.
) else (

    REM The command failed
    echo Error: %errorlevel%.
)

pause
