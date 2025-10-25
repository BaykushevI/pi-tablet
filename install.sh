#!/bin/bash

echo "Installing Pi Tablet dependencies..."
echo ""

# Update system
echo "Updating system..."
sudo apt-get update -qq

# Install dependencies
echo "Installing system packages..."
sudo apt-get install -y python3-pip python3-dev build-essential \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    pkg-config libgl1-mesa-dev libgles2-mesa-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    libraspberrypi-bin xinput

# Install Python packages
echo "Installing Python packages..."
pip3 install --upgrade pip
pip3 install kivy requests psutil

# Setup autostart
echo "Setting up autostart..."
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/pi_tablet.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Pi Tablet
Exec=/usr/bin/python3 /home/ibayk/pi-tablet/pi_tablet.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

echo "PI Tablet installation complete. The application will start automatically on next boot."
