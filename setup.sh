#!/bin/bash

clear
echo " PI Tablet automatic installl

if[ ! - f "py_tablet"]; then
    echo "Downloading PI Tablet..."
    exit 1
fi

echo "Installing PI Tablet..."

if command -v git &> /dev/null; then
    echo "Git found, cloning repository..."
else
    echo "Installing Git..."
    sudo apt-get update -qq
    sudo apt-get install -y git
fi

# Check if Python3 is installed
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "Python3 found. Version: $PYTHON_VERSION"
else
    echo "Installing Python3..."
    sudo apt-get update -qq
    sudo apt-get install -y python3 python3-venv python3-pip
fi

echo " Install dependencies..."

# Update environment
sudo apt-get update -qq

# Install required packages
sudo apt-get install -y -qq \
    python3-pip \
    python3-dev \
    build-essential \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    pkg-config \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    python3-setuptools \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-alsa \
    libmtdev-dev \
    xclip \
    xsel \
    libjpeg-dev \
    libraspberrypi-bin \
    xinput

echo "System packages installed."

# Upgrade pip
echo "Upgrading pip..."
pip3 install --upgrade pip -qq

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Python environment setup complete."
else
    echo "Error installing Python dependencies."
    exit 1
fi

echo "Configuring PI Tablet..."

# Set executable permissions
chmod +x py_tablet.py backup.sh install.sh 2> /dev/null
echo "Permissions set."

# Autostart configuration
echo "Setting up autostart..."
mkdir -p ~/.config/autostart

cat > ~/.config/autostart/py_tablet.desktop << E0F
[Desktop Entry]
Type=Application
Name=PI Tablet
Exec=sh -c 'sleep 10 && /usr/bin/python3 $(pwd)/py_tablet.py'
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
E0F

echo "Autostart configured."

# Create backup directory
mkdir -p ~/pi_tablet_backups
echo "Backup directory created at ~/pi_tablet_backups."

echo "APi Key Setup"

# Check for API if is present
if grep -q "baeab5723c721975319ad6f192d1c90b" pi_tablet.py; then
    echo "Default API key not found. Please enter your OpenAI API key!"
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your API Key: " API_KEY
        if [ ! -z "$API_KEY" ]; then  
            #replace API Key in file
            sed -i "s/baeab5723c721975319ad6f192d1c90b/$API_KEY/g" py_tablet.py
            echo "API Key updated successfully."
        else
            echo "Skipping API key update. You can update it later in py_tablet.py."
        fi
    else
        echo "You can update your API key later in py_tablet.py if needed."
    fi
else
    echo "Custom API key already set."
fi 

echo "Installation complete! Please restart your Raspberry Pi to apply all changes."
read -p "Do you want to restart now? (y/n): " -n 1 -r
echo    # move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Restarting..."
    sleep 2
    python3 py_tablet.py
else
    echo "Start when you are ready."
    echo " python3 pi_tablet.py"
fi