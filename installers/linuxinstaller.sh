#!/bin/bash

# colors for text, needed for actually reading the text lol
RED='\033[0;31m' 
GREEN='\033[0;32m'
NC='\033[0m'

# functions go down here, just learned these thanks to Phind.
PYInstall() { # installs python and pip, what else did you expect?
    if command -v pacman > /dev/null; then
        echo -e "${GREEN}installing python and pip with pacman...${NC}"; sleep 3
        sudo pacman -S python python-pip
    elif command -v dnf > /dev/null; then
        echo -e "${GREEN}installing python and pip with dnf...${NC}"; sleep 3
        sudo dnf install python python-pip
    elif command -v apt > /dev/null; then
        echo -e "${GREEN}installing python and pip with apt...${NC}"; sleep 3
        sudo apt install python3 python3-pip
    else
        echo -e "${RED}you don't have pacman, apt or apt!!! what are you using???!! (just install python manually!!!)${NC}"
    fi
}

GITFail() { # if the clone command doesn't work, it will run this
    if command -v git > /dev/null; then # runs if the command exists, and also if its output is true
        echo -e "${GREEN}git is already installed, retrying clone...${NC}";git clone https://github.com/soswav/bigrat.git
    else # if any of the above is NOT true then it will run stuff below
        if command -v pacman > /dev/null; then
            echo -e "${GREEN}Installing git with pacman...${NC}"; sleep 3
            sudo pacman -S git && git clone https://github.com/soswav/bigrat.git
        elif command -v dnf > /dev/null; then # if first thing  wans't true but this other thing is true then do this
            echo -e "${GREEN}Installing git with dnf...${NC}"; sleep 3
            sudo dnf install git && git clone https://github.com/soswav/bigrat.git
        elif command -v apt > /dev/null; then
            echo -e "${GREEN}Installing git with apt...${NC}"; sleep 3
            sudo apt install git && git clone https://github.com/soswav/bigrat.git
        else
            echo -e "${RED}you don't have pacman, dnf or apt!! install git manually because i don't know what you're using!${NC}"
        fi
    fi
}

REQ() {
   if command -v pip > /dev/null; then
        echo -e "${GREEN}pip is already installed, installing dependencies!${NC}";pip install discord requests PyYAML
   else
       if command -v pacman > /dev/null; then
            echo -e "${RED}you don't have pip! trying to install with pacman...${NC}"; sleep 3
            sudo pacman -S pip && pip install discord requests PyYAML
       elif command -v dnf > /dev/null; then
            echo -e "${RED}you don't have pip! trying to install with dnf...${NC}"; sleep 3
            sudo dnf install pip && pip install discord requests PyYAML
       elif command -v apt > /dev/null; then
            echo -e "${RED}you don't have pip! trying to install with dnf...${NC}"; sleep 3
            sudo apt install pip && pip install discord requests PyYAML
       else
            echo -e "${RED}you don't have neither pacman, dnf, or apt! install pip manually you prick!${NC}"
       fi
    fi
}

activate_venv() {
    local env_name=${1:-".venv"}

    if [ ! -d "$env_name" ]; then
        echo -e "${RED}virtual environment '$env_name' not found! creating one...${NC}"
        python -m venv $env_name
    fi

    source $env_name/bin/activate
}
# leaving funcion zone so early?

clear # clears the terminal so its more readeable
while true; do
    read -p "do you have python & pip already installed? (y/n)" choice
    case "$choice" in 
     [yY]* ) 
       echo -e "${GREEN}alrighty!${NC}"
       break
       ;;
     [nN]* )
       PYInstall
       break
       ;;
    esac
done

sleep 3; clear
# this is something you should actually read, pal!
echo -e "${GREEN}i would like to mention that you need to toggle some stuff on discord.com/developers before continuing"
echo -e "${GREEN}go to your bot, then search for 'Privileged Gateway Intents' on the bot tab, toggle everything you see there"
echo -e "${RED}i'm going to make you wait 10 seconds to make sure you read all this, sorry!${NC}"; sleep 10


clear # clears the terminal for better reability!
cd ~/bigrat && echo -e "${RED}folder exists, deleting with sudo${NC}"; sudo rm -r ~/bigrat/ # checks if you already installed bigrat
sleep 1; clear; cd ~/ # makes sure you read that, smh!
echo -e "${GREEN}cloning git repo...${NC}"; git clone https://github.com/soswav/bigrat.git || GITFail # notifies user that it's going to clone the repo, if it fails it runs the GITFail function
clear

echo -e "${GREEN}generating a venv with python...${NC}";activate_venv "~/bigrat/.venv";sleep 3;clear
echo -e "${GREEN}installing bot requirements with pip...${NC}";sleep 3;REQ
echo -e "${GREEN}git clone, requirements installation and creation of venv finished! sending to directory...${NC}";cd ~/bigrat;sleep 2 # You can guess, bucko!
clear;echo -e "${GREEN}opening config.yml for edit in 5 secs, make sure to fill the spots...${NC}";sleep 5;nano ~/bigrat/config.yml # editor

while true; do
    read -p "do you want to edit the bot.py file? (y/n)" choice
    case "$choice" in 
     [yY]* ) 
       echo -e "${GREEN}editing bot.py with nano...${NC}";sleep 1;nano ~/bigrat/bot.py
       break
       ;;
     [nN]* )
       echo -e "${GREEN}alright, skipping...${NC}"
       break
       ;;
    esac
done

while true; do
    read -p "do you want to run the bot right now? (y/n)" choice
    case "$choice" in 
     [yY]* ) 
       echo -e "${GREEN}running bot.py...${NC}";sleep 1;python ~/bigrat/bot.py;sleep 2
       break
       ;;
     [nN]* )
       echo -e "${GREEN}okay, later i guess...${NC}"
       break
       ;;
    esac
done

clear;echo -e "${GREEN}bigrat discord bot succefully setup! (probably!)${NC}";sleep 2
