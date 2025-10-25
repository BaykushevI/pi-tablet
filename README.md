# Raspberry Pi Tablet Dashboard
A minimal, elegant dashboard for Raspberry Pi 5 with a 7" touchscreen display (1024x600).
Perfect for your desk - displays time, weather, and system stats.

## Features
3 Clean Screens:
Screen      Description
Clock       Time, date, current temperature
Weather     5-day forecast + current conditions
System      CPU, RAM, Pi temperature, disk usage

**Capabilities:**
- Swipe navigation between screens
- Auto dim at night (11pm-7am)
- Dark theme optimized for 7" display
- Auto-start on boot
- Touch optimized interface

## Requirements
**Hardware:**
- Raspberry Pi 5 (also works with Pi 4)
- 7" touchscreen display 1024x600 IPS
- 16GB+ microSD card
- Internet connection

**Software:**
- Raspberry Pi OS (Bookworm or newer)
- Python 3.9+
- Git

## Installation (3 Steps)
Step 1: Clone the repository on your Pi
cd ~
git clone https://github.com/YOUR_USERNAME/pi-tablet.git
cd pi-tablet

Step 2: Run automatic installer
chmod +x setup.sh
./setup.sh

The script will:
- Install all dependencies (10-15 minutes)
- Set up auto-start
- Ask for your API key

Step 3: Add your weather API key
- Sign up at OpenWeatherMap (free) https://openweathermap.org/api
- Copy your API key
- Edit the file:
nano pi_tablet.py
Find line ~26:
OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"
Replace with your key:
OPENWEATHER_API_KEY = "abc123def456"
Save: Ctrl+O, Enter, Ctrl+X
That's it! Start the app:
python3 pi_tablet.py

## Usage
**Starting:**
cd ~/pi-tablet
python3 pi_tablet.py

**Navigation:**
Swipe left → next screen
Swipe right → previous screen

**Fullscreen mode:**
Add to pi_tablet.py:
Window.fullscreen = 'auto'

## Configuration
Edit pi_tablet.py (lines 20-26):
WINDOW_SIZE = (1024, 600)    # Window size
NIGHT_MODE_START = 23        # Night mode start (11pm)
NIGHT_MODE_END = 7           # Night mode end (7am)
LOCATION = "Sofia"           # Your city
OPENWEATHER_API_KEY = "..."  # Your API key

## Updating
cd ~/pi-tablet
git pull
pip3 install --upgrade -r requirements.txt
python3 pi_tablet.py

## Troubleshooting
Weather not showing?
- Check API key and internet connection
Touch not working?
sudo apt-get install xinput-calibrator
xinput_calibrator
Kivy installation error?
sudo apt-get install -y libsdl2-dev
pip3 install --upgrade kivy

## Project Structure
pi-tablet/
─ pi_tablet.py         # Main application
─ requirements.txt     # Python dependencies
─ setup.sh             # Auto installer
─ .gitignore           # Git ignore rules
─ README.md            # This file

## Development
Add a new screen:
pythonclass MyScreen(Screen):
    def __init__(self, **kwargs):
        super(MyScreen, self).__init__(**kwargs)
        # Your code

# In PiTabletApp.build():
sm.add_widget(MyScreen(name='myscreen'))
Update the screens list:
pythonscreens = ['clock', 'weather', 'system', 'myscreen']

**Repository:** https://github.com/BaykushevI/job-scheduler-ga
