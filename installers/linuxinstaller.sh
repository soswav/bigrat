#!/bin/bash

# colors for text, needed for actually reading the text lol
RED='\033[0;31m' 
GREEN='\033[0;32m'
ASCII='\033[1;33m' # it's yellowish!
NC='\033[0m'

# functions go down here, just learned these thanks to Phind!
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
            echo -e "${GREEN}installing git with pacman...${NC}";sleep 3
            sudo pacman -S git && git clone https://github.com/soswav/bigrat.git
        elif command -v dnf > /dev/null; then # if first thing  wans't true but this other thing is true then do this
            echo -e "${GREEN}installing git with dnf...${NC}";sleep 3
            sudo dnf install git && git clone https://github.com/soswav/bigrat.git
        elif command -v apt > /dev/null; then
            echo -e "${GREEN}installing git with apt...${NC}";sleep 3
            sudo apt install git && git clone https://github.com/soswav/bigrat.git
        else
            echo -e "${RED}you don't have pacman, dnf or apt!! install git manually because i don't know what you're using!${NC}"
        fi
    fi
}

REQ() {
   if command -v pip > /dev/null; then
        echo -e "${GREEN}installing dependencies for the bot...${NC}";pip install discord requests PyYAML asyncio
   else
       if command -v pacman > /dev/null; then
            echo -e "${RED}you don't have pip! trying to install with pacman...${NC}"; sleep 3
            sudo pacman -S pip && pip install discord requests PyYAML asyncio
       elif command -v dnf > /dev/null; then
            echo -e "${RED}you don't have pip! trying to install with dnf...${NC}"; sleep 3
            sudo dnf install pip && pip install discord requests PyYAML asyncio
       elif command -v apt > /dev/null; then
            echo -e "${RED}you don't have pip! trying to install with dnf...${NC}"; sleep 3
            sudo apt install pip && pip install discord requests PyYAML asyncio
       else
            echo -e "${RED}you don't have neither pacman, dnf, or apt! install pip manually you prick!${NC}"
       fi
    fi
}

activate_venv() {
    local env_name=${1:-".venv"}

    if [ ! -d "$env_name" ]; then
        echo -e "${RED}virtual environment '$env_name' not found! creating one...${NC}"
        python -m venv "$env_name"
    fi

    source "$env_name"/bin/activate
}

ascii(){
    clear;echo -e "${ASCII}
                                                                                                               powered by soswav
  ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗     ███████╗██████╗    ███████╗██╗  ██╗
  ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║     ██╔════╝██╔══██╗   ██╔════╝██║  ██║
  ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║     █████╗  ██████╔╝   ███████╗███████║
  ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║     ██╔══╝  ██╔══██╗   ╚════██║██╔══██║
  ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗███████╗██║  ██║██╗███████║██║  ██║
  ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
                                     The big rat quick installer for computers running Linux!${NC}
    "
}
# leaving funcion zone so early?

ascii;sleep 3 # clears the terminal so its more readeable
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

sleep 3;ascii
echo -e "${RED}NOTE: you should read the wiki as it contains info on what the bot needs! 
i'm going to make you wait 10 seconds to make sure you read this, sorry!${NC}";sleep 10


ascii
cd "$HOME/bigrat" && echo -e "${RED}folder exists, deleting...${NC}";rm -rf "$HOME/bigrat/" # checks and deletes for bigrat folder
sleep 1;ascii;cd "$HOME" || exit # makes sure you read
echo -e "${GREEN}cloning git repo...${NC}";git clone https://github.com/soswav/bigrat.git || GITFail # notifies user that it's going to clone the repo, if it fails it runs the GITFail function
ascii

echo -e "${GREEN}generating a venv with python...${NC}";activate_venv "$HOME/bigrat/.venv";sleep 3;REQ;sleep 3
echo -e "${GREEN}git clone, installation of pip packages and creation of venv finished! sending to directory...${NC}";cd "$HOME/bigrat";sleep 2
ascii;echo -e "${GREEN}opening config.yml for edit in 5 secs, make sure to fill the spots...${NC}";sleep 5;nano "$HOME/bigrat/config.yml" # editor

while true; do
    read -p "do you want to edit the bot.py file? (y/n)" choice
    case "$choice" in 
     [yY]* ) 
       echo -e "${GREEN}editing bot.py with nano...${NC}";sleep 1;nano "$HOME/bigrat/bot.py"
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
       echo -e "${GREEN}running bot.py...${NC}";sleep 1;python "$HOME/bigrat/bot.py";sleep 2
       break
       ;;
     [nN]* )
       echo -e "${GREEN}okay, later i guess...${NC}"
       break
       ;;
    esac
done

ascii;echo -e "${GREEN}bigrat discord bot succefully setup! (probably!)${NC}";sleep 3
