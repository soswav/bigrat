#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

clear

read -p "do you want to install 'lolcat'? it's required for some rainbow text (y/n):" choice
case "$choice" in 
 [yY]* ) 
   echo -e "${GREEN}installing the 'lolcat' dependencies${NC}"
   sudo pacman -S lolcat && sudo apt install lolcat && sudo dnf install lolcat
   ;;
 * ) 
   echo -e "${GREEN}okay, sorry for asking!${NC}"
   ;;
esac
# echo -e "${GREEN}installing dependencies for rainbow text, not required but it will look cool as hell!${NC}" && 
sleep 2
clear
cd ~/bigrat && echo -e "${RED}folder exists, deleting with sudo${NC}" && sudo rm -r ~/bigrat/
cd ~/
echo -e "${GREEN}cloning git repo...${NC}"
echo -e "${GREEN}cloning git repo...${NC}"
(git clone https://github.com/soswav/bigrat.git || (echo -e "${RED}no git? trying to install with pacman...${NC}" && sudo pacman -S git || (echo -e "${RED}didn't work, trying dnf...${NC}" && sudo dnf install git))) || (echo -e "${RED}didn't work, trying apt...${NC}" && sudo apt install git)

echo -e "${GREEN}git clone finished! sending to cloned directory...${NC}"
cd ~/bigrat || echo -e "${RED}folder doesn't exist${NC}"

echo -e "${GREEN}opening config.json for edit, make sure to fill the spots...${NC}"
sleep 5
nano config.json

clear
echo -e "bigrat discord bot succefully setup!" | lolcat -a

read -p "do you want to run the bot right now? (y/n):" choice
case "$choice" in 
 [yY]* ) 
   echo -e "${GREEN}running bot.py...${NC}"
   python ~/bigrat/bot.py || echo -e "${RED}no python? trying to install with pacman...${NC}" && sudo pacman -S python || clear && echo -e "${RED}didn't work, trying dnf...${NC}" && sudo dnf install python || echo -e "${RED}didn't work, trying apt...${NC}" && sudo apt install python
   ;;
 * ) 
   echo -e "${GREEN}okay, later i guess...${NC}"
   ;;
esac
