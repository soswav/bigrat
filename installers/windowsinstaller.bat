@echo off
cls


REM Set the variables for the paths and commands
set discord_module=discord.py
set title=wawas's installer of the modules!


REM Set the title of the console window
title %title%


REM Install the discord module using pip
echo Installing %discord_module%...
pip install %discord_module%


REM Check the error level of the previous command
if %errorlevel% equ 0 (

    REM The command was successful
    echo Done.
) else (

    REM The command failed
    echo Error: %errorlevel%.
)


REM Pause the script and wait for user input
pause
