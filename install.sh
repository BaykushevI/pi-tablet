#!/bin/bash

echo "Installing PI Tablet ..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install python dependencies
echo "Installing Python dependencies..."
sudo apt-get install -y python3-pip python3-dev build-essential
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
sudo apt-get install -y pkg-config libgl1-mesa-dev libgles2-mesa-dev
sudo apt-get install -y python3-setuptools libgstreamer1.0-dev git-core
sudo apt-get install -y gstreamer1.0-plugins-{bad,base,good,ugly}
sudo apt-get install -y gstreamer1.0-{omx,alsa} python3-dev libmtdev-dev
sudo apt-get install -y xclip xsel libjpeg-dev

# Install pip packages
echo "Installing required Python packages..."
pip3 install --upgrade pip
pip3 install -r reuirements.txt

# Create autostart script
echo "Creating autostart script..."
mkdir -p ~/.config/autostart

cat > ~/.config/autostart/pi_tablet.desktop << E0F
[Desktop Entry]
Type=Application
Name=PI Tablet
Exec=/usr/bin/python3 $(pwd)/pi_tablet.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
E0F

# Runnable script created
chmod -x pi_tablet.py

echo "PI Tablet installation complete. The application will start automatically on next boot."