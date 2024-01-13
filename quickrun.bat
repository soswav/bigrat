@echo off
cls


REM Set the variables for the paths and commands
set bot_path=bot.py
set title=wawa's launcher


REM Set the title of the console window without changing the directory
title %title%


REM Run the bot script using python
python %bot_path%


REM Check the error level of the previous command
if %errorlevel% equ 0 (

    REM The command was successful
    echo /C Bot started successfully. /Q
) else (

    REM The command failed
    echo /C Bot failed to start. /Q
)


REM Pause the script and wait for user input
pause
