#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

clear

cd ~/
echo -e "${GREEN}cloning git repo...${NC}"
git clone https://github.com/soswav/bigrat.git || echo -e "${RED}no git? trying to install with pacman...${NC}" && sudo pacman -S git || echo -e "${RED} didn't work, trying dnf...${NC}" && sudo dnf install git || echo -e "${RED}didn't work, trying apt...${NC}" && sudo apt install git

echo -e "${GREEN}git clone finished! sending to cloned directory...${NC}"
cd ~/bigrat || echo -e "${RED}fatal: destination path 'bigrat' already exists and is not an empty directory${NC}"

echo -e "${GREEN}opening config.json for edit...${NC}"
nano config.json

echo -e "${GREEN}running bot.py...${NC}"
python ~/bigrat/bot.py || echo -e "${RED}no python? trying to install with pacman...${NC}" && sudo pacman -S python || clear && echo -e "${RED}didn't work, trying dnf...${NC}" && sudo dnf install python || echo -e "${RED}didn't work, trying apt...${NC}" && sudo apt install python

clear && echo -e "${GREEN}bigrat discord bot succefully setup!${NC}"
