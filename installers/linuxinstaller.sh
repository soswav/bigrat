#!/bin/bash

# colors for text, needed for actually reading the text lol
RED='\033[0;31m' 
GREEN='\033[0;32m'
NC='\033[0m'

clear # clears the terminal so its more readeablle

read -p "do you have python & pip already installed? (y/n)" choice
case "$choice" in 
 [yY]* ) 
   echo -e "${GREEN}alrighty!${NC}"
   ;;
 * ) 
   echo -e "${GREEN}installing python and pip with pacman...${NC}"
   sudo pacman -S python python-pip || echo -e "${RED}didn't work, trying dnf...${NC}" && sleep 2 && sudo dnf install python python-pip || echo -e "${RED}didn't work, trying apt...${NC}" && sleep 2 && sudo apt install python3 python3-pip
   ;;
esac

sleep 3 && clear
echo -e "${GREEN}i would like to mention that you need to toggle some stuff on discord.com/developers before continuing${NC}"
echo -e "${GREEN}go to your bot, then search for 'Privileged Gateway Intents' on the bot tab, toggle everything you see there${NC}"
echo -e "${RED}i'm going to make you wait 10 seconds to make sure you read all this, sorry!${NC}"
sleep 10


sleep 2 && clear # takes two seconds then clears
cd ~/bigrat && echo -e "${RED}folder exists, deleting with sudo${NC}" && sudo rm -r ~/bigrat/ # checks if you already installed bigrat
sleep 1 && clear
cd ~/
echo -e "${GREEN}cloning git repo...${NC}"
git clone https://github.com/soswav/bigrat.git || (echo -e "${RED}no git? trying to install with pacman...${NC}" && sudo pacman -S git && echo -e "${GREEN}installed! retrying...${NC}" && git clone https://github.com/soswav/bigrat.git) || (echo -e "${RED}didn't work, trying dnf...${NC}" && sudo dnf install git && echo -e "${GREEN}installed! retrying...${NC}" && git clone https://github.com/soswav/bigrat.git) || (echo -e "${RED}didn't work, trying apt...${NC}" && sudo apt install git && echo -e "${GREEN}installed! retrying...${NC}" && git clone https://github.com/soswav/bigrat.git)

read -p "quick question, are you using fish? (y/n)" choice
case "$choice" in
 [yY]* )
   echo -e "${GREEN}kk! generating venv with python!${NC}"
   python -m venv ~/bigrat/.venv && source ~/bigrat/.venv/bin/activate.fish
   ;;
 * )
   echo -e "${GREEN}alrightyy!!! generating a venv with python!${NC}"
   python -m venv ~/bigrat/.venv && source ~/bigrat/.venv/bin/activate
   ;;
esac

echo -e "${GREEN}git clone & creation of venv finished! sending to directory...${NC}"
cd ~/bigrat # sends to directory

echo -e "${GREEN}installing bot requirements with pip...${NC}" && sleep 3
pip install discord requests PyYAML asyncio || echo -e "${RED}didn't work, trying with 'pip3'${NC}" && pip3 install discord requests PyYAML

echo -e "${GREEN}opening config.yml for edit in 5 secs, make sure to fill the spots...${NC}" && sleep 5
nano ~/bigrat/config.yml # editor

read -p "do you want to check the bot.py file? (y/n)" choice
case "$choice" in 
 [yY]* ) 
   echo -e "${GREEN}editing bot.py with nano...${NC}"
   nano ~/bigrat/bot.py
   ;;
 * ) 
   echo -e "${GREEN}alright, skipping...${NC}"
   ;;
esac

read -p "do you want to run the bot right now? (y/n):" choice
case "$choice" in 
 [yY]* ) 
   echo -e "${GREEN}running bot.py...${NC}"
   python ~/bigrat/bot.py
   ;;
 * ) 
   echo -e "${GREEN}okay, later i guess...${NC}"
   ;;
esac

clear
echo -e "${GREEN}bigrat discord bot succefully setup! (maybe!)${NC}" && sleep 2
