#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}cloning git repo...${NC}"
if ! git clone https://github.com/soswav/bigrat.git; then
   echo -e "${RED}no git? trying to install with pacman...${NC}"
   sudo pacman -S git || echo -e "${RED} didn't work, trying dnf...${NC}" && sudo dnf install git || echo -e "${RED}didn't work, trying apt...${NC}" && sudo apt install git
fi
echo -e "${GREEN}git clone finished! sending to cloned directory...${NC}"
cd ~/bigrat

echo -e "${GREEN}opening config.json for edit...${NC}"
nano config.json

echo -e "${GREEN}running bot.py...${NC}"
python ~/bigrat/bot.py

echo -e "${RED}no python? trying to install with pacman...${NC}"
sudo pacman -S python || echo -e "${RED}didn't work, trying dnf...${NC}" && sudo dnf install python || echo -e "${RED}didn't work, trying apt...${NC}" && sudo apt install python
