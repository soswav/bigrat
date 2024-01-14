#!/bin/bash

# colors for text, needed for actually reading the text lol
RED='\033[0;31m' 
GREEN='\033[0;32m'
NC='\033[0m'

clear # clears the terminal so its more readeablle

# asks if you want to install lolcat, y/n question if first install fails it will try with other package managers until it gets yours right
read -p "do you want to install 'lolcat'? it's required for rainbow color in install (y/n):" choice
case "$choice" in 
 [yY]* ) 
   echo -e "${GREEN}installing lolcat with pacman...${NC}"
   sudo pacman -S lolcat || echo -e "${RED}didn't work, trying dnf...${NC}" && sleep 2 && sudo dnf install lolcat || echo -e "${RED}didn't work, trying apt...${NC}" && sleep 2 && sudo apt install lolcat
   ;;
 * ) 
   echo -e "${GREEN}okay, sorry for asking!${NC}"
   ;;
esac

sleep 2 && clear # takes two seconds then clears
cd ~/bigrat && echo -e "${RED}folder exists, deleting with sudo${NC}" && sudo rm -r ~/bigrat/ # checks if you already installed bigrat
cd  ~/
echo -e "${GREEN}cloning git repo...${NC}"
git clone https://github.com/soswav/bigrat.git || (echo -e "${RED}no git? trying to install with pacman...${NC}" && sudo pacman -S git && echo -e "${GREEN}installed! retrying...${NC}" && git clone https://github.com/soswav/bigrat.git) || (echo -e "${RED}didn't work, trying dnf...${NC}" && sudo dnf install git && echo -e "${GREEN}installed! retrying...${NC}" && git clone https://github.com/soswav/bigrat.git) || (echo -e "${RED}didn't work, trying apt...${NC}" && sudo apt install git && echo -e "${GREEN}installed! retrying...${NC}" && git clone https://github.com/soswav/bigrat.git)

echo -e "${GREEN}git clone finished! sending to directory...${NC}"
cd ~/bigrat # sends to directory

echo -e "${GREEN}installing bot requirements with pip...${NC}" && sleep 3
pip install discord requests PyYAML

echo -e "${GREEN}opening config.yml for edit in 5 secs, make sure to fill the spots...${NC}"
sleep 5
nano ~/bigrat/bot/config.yml # text editor for terminals

read -p "do you want to check the bot.py file? (y/n)" choice
case "$choice" in 
 [yY]* ) 
   echo -e "${GREEN}editing bot.py with nano...${NC}"
   nano ~/bigrat/bot/bot.py
   ;;
 * ) 
   echo -e "${GREEN}alright, skipping...${NC}"
   ;;
esac

read -p "do you want to run the bot right now? (y/n):" choice
case "$choice" in 
 [yY]* ) 
   echo -e "${GREEN}running bot.py...${NC}"
   python ~/bigrat/bot/bot.py || echo -e "${RED}no python? trying to install with pacman...${NC}" && sudo pacman -S python && echo -e "${GREEEN}installed! retrying...${NC}" && python ~/bigrat/bot/bot.py || echo -e "${RED}didn't work, trying dnf...${NC}" && sleep 2 && sudo dnf install python && echo -e "${GREEEN}installed! retrying...${NC}" && python ~/bigrat/bot/bot.py || echo -e "${RED}didn't work, trying apt...${NC}" && sleep 2 && sudo apt install python && echo -e "${GREEEN}installed! retrying...${NC}" && python ~/bigrat/bot/bot.py
   ;;
 * ) 
   echo -e "${GREEN}okay, later i guess...${NC}"
   ;;
esac

clear
echo -e "bigrat discord bot succefully setup!" | lolcat -a
