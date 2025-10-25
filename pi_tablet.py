#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Raspberry Pi Tablet Application
"""

import os 
os.environ['KIVY_NO_ARGS'] = '1'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from datetime import datetime, timedelta
import requests
import json
import sqlite3
import psutil
import subprocess


# Settings
WINDOW_Size = (1024,600)
NIGHT_MODE_START = 23
NIGHT_MODE_END = 7
STANDBY_TIMEOUT = 30
LOCATION = "Sofia"
OPENWEATHER_API_KEY = "baeab5723c721975319ad6f192d1c90b"

# Database
def init_database():
    conn = sqlite3.connect('pi_tablet.db')
    c = conn.cursor()

    # Table for shopiing lists
    c.execute('''CREATE TABLE IF NOT EXISTS shopping_lists
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 items TEXT,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 completed INTEGER DEFAULT 0)''')
    
    # Table for reminders
    c.execute('''CREATE TABLE IF NOT EXISTS reminders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 text TEXT NOT NULL,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 priority TEXT DEFAULT 'normal')''')
    
    conn.commit()
    conn.close()

# Main screen - Clock
class ClockScreen(Screen):
    def __init__(self, **kwargs):
        super(ClockScreen, self).__init__(**kwargs)
        self.layout = FloatLayout()

        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.15, 1)  # Black background
            self.rect = Rectangle(size=WINDOW_Size, pos=self.layout.pos)

        # Digital Clock
        self.time_label = Label(
            text = '00:00',
            font_size = '120sp',
            color = (0.9, 0.9, 1, 1),
            pos_hint = {'center_x': 0.5, 'center_y': 0.6}
        )

        # Date Label
        self.date_label = Label(
            text = '',
            font_size = '32sp',
            color = (0.7, 0.7, 0.8, 1),
            size_hint = (1, 0.2),
            pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        )

        # Weather Label
        self.temp_label = Label(
            text = '--°C',
            font_size = '48sp',
            color = (0.7, 0.8, 0.9, 1),
            size_hint = (1, 0.2),
            pos_hint = {'center_x': 0.5, 'center_y': 0.25}
        )

        # Instructions Label
        info_label = Label(
            text = 'Swipe left or right to navigate',
            font_size = '14sp',
            color = (0.5, 0.5, 0.6, 1),
            size_hint = (1, 0.1),
            pos_hint = {'center_x': 0.5, 'y': 0.05}
        )

        self.layout.add_widget(self.time_label)
        self.layout.add_widget(self.date_label)
        self.layout.add_widget(self.temp_label)
        self.layout.add_widget(info_label)
        self.add_widget(self.layout)

        # Refresh 
        Clock.schedule_interval(self.update_time, 1)
        Clock.schedule_interval(self.update_weather, 1800)
        self.update_weather(0)
    
    def update_time(self, dt):
        now = datetime.now()
        self.time_label.text = now.strftime('%H:%M')
        
        # Month and Day
        month_day = ["January", "February", "March", "April", "May", "June",
                     "July", "August", "September", "October", "November", "December"]
                     
        days_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]  

        month_name = month_day[now.month - 1]
        day_name = days_week[now.weekday()]

        self.date_label.text = f"{day_name}, {now.day} {month_name} {now.year}"

    def update_weather(self, dt):
        try:
            if OPENWEATHER_API_KEY == "baeab5723c721975319ad6f192d1c90b":
                self.temp_label.text = "API Key Missing"
                return
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200:
                temp = round(data['main']['temp'])
                self.temp_label.text = f"{temp}°C"
        except:
            self.temp_label.text = "--°C"

# Weather screen
class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation = 'vertical', padding = 20, spacing = 15)

        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.15, 1)  # Black background
            self.rect = Rectangle(size = Window.size, pos = self.layout.pos)

        # Weather Info Label
        title = Label(
            text = 'Loading weather...',
            font_size = '36sp',
            bold = True,
            size_hint_y = 0.15,
            color = (0.9, 0.9, 1, 1)
        )
        self.layout.add_widget(title)

        # Current time
        self.current_weather = Label(
            text = 'Current: --°C, --',
            font_size = '24sp',
            size_hint_y = 0.25,
            color = (0.8, 0.9, 1, 1)
        )
        self.layout.add_widget(self.current_weather)

        # 5 day forecast
        self.forecast_layout = GridLayout(cols = 5, spacing = 10, size_hint_y = 0.6)
        self.layout.add_widget(self.forecast_grid)

        self.add_widget(self.layout)

        Clock.schedule_interval(self.update_weather, 1800)
        self.update_weather(0)

    def update_weather(self, dt):
        try:
            if OPENWEATHER_API_KEY == "baeab5723c721975319ad6f192d1c90b":
                self.current_weather.text = "API Key Missing"
                return
            
            # Current weather
            url = f"http://api.openweathermap.org/data/2.5/weather?q={LOCATION}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url, timeout = 10)
            data = response.json()

            if response.status_code == 200:
                temp = round(data['main']['temp'])
                feels_like = round(data['main']['feels_like']) 
                desc = data['weather'][0]['description'].capitalize()
                humidity = data['main']['humidity']
                wind = round(data['wind']['speed'] * 3.6)  # Convert m/s to km/h

                self.current_weather.text = (
                    f"Current: {temp}°C (Feels like {feels_like}°C), {desc}\n"
                    f"Humidity: {humidity}%, Wind: {wind} km/h"
                )

            # 5 day forecast
            url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={LOCATION}&appid={OPENWEATHER_API_KEY}&units=metric"
            response_forecast = requests.get(url_forecast, timeout = 10)
            data_forecast = response_forecast.json()

            if response_forecast.status_code == 200:
                # Clear previous forecast
                self.forecast_layout.clear_widgets()

                # Get one refresh per day
                daily_forecast = []
                current_date = None

                for item in data_forecast['list']:
                    date_txt = item['dt_txt']
                    date = dt_text.split()[0]
                    time = dt_text.split()[1]

                    if date != current_date and time == "12:00:00":
                        daily_forecast.append(item)
                        current_date = date

                    if len(daily_forecast) >= 5:
                        break

                for forecast in daily_forecast:
                    day_widget = self.create_day_widget(forecast)
                    self.forecast_layout.add_widget(day_widget)
        except Exception as e:
            self.current_weather.text = "Error loading weather"

    def create_day_widget(self, forecast):
        layout = BoxLayout(orientation = 'vertical', padding = 5)

        # Day Label
        date = datetime.strptime(forecast['dt_txt'], '%Y-%m-%d %H:%M:%S')
        days_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        day_name = days_week[date.weekday()]

        day_label = Label(
            text = f"{day_name}\n{date.day}.{date.month}",
            font_size = '16sp',
            size_hint_y = 0.3,
            color = (0.9, 0.9, 1, 1)
        )

        # Temp Label
        temp = round(forecast['main']['temp'])
        temp_label = Label(
            text = f"{temp}°C",
            font_size = '24sp',
            bold = True,
            size_hint_y = 0.4,
            color = (0.8, 0.9, 1, 1)
        )

        # Description Label
        desc = forecast['weather'][0]['description'].capitalize()
        desc_label = Label(
            text = desc,
            font_size = '12sp',
            size_hint_y = 0.3,
            color = (0.7, 0.8, 0.9, 1)
        )

        layout.add_widget(day_label)
        layout.add_widget(temp_label)
        layout.add_widget(desc_label)

        return layout
    
# Shopping List Screen
# TODO 

# Google Calendar Screen
# TODO

# System information Screen
class SystemScreen(Screen):
    def __init__(self, **kwargs):
        super(SystemScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation = 'vertical', padding = 20, spacing = 15)

        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.15, 1)  # Black background
            self.rect = Rectangle(size = Window.size, pos = self.layout.pos)

        # Title Label
        title = Label(
            text = 'System Information',
            font_size = '36sp',
            bold = True,
            size_hint_y = 0.15,
            color = (0.9, 0.9, 1, 1)
        )
        self.layout.add_widget(title)

        # Info Labels
        self.cpu_label = Label(
            text = 'CPU Usage: --%',
            font_size = '24sp',
            size_hint_y = 0.2,
            color = (0.8, 0.9, 1, 1)
        )
        self.layout.add_widget(self.cpu_label)

        self.memory_label = Label(
            text = 'Memory Usage: --%',
            font_size = '24sp',
            size_hint_y = 0.2,
            color = (0.8, 0.9, 1, 1)
        )
        self.layout.add_widget(self.memory_label)

        self.disk_label = Label(
            text = 'Disk Usage: --%',
            font_size = '24sp',
            size_hint_y = 0.2,
            color = (0.8, 0.9, 1, 1)
        )
        self.layout.add_widget(self.disk_label)

        self.add_widget(self.layout)

        Clock.schedule_interval(self.update_system_info, 5)
        self.update_system_info(0)

    def update_system_info(self, dt):
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval = 1)
            cpu_freq = psutil.cpu_freq()

            # RAM
            ram = psutil.virtual_memory()
            ram_used = ram.used / (1024 ** 3)  # in GB
            ram_total = ram.total / (1024 ** 3)  # in GB
            ram_percent = ram.percent

            # Temp
            try:
                temp_output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
                temp_c = float(temp_output.split('=')[1].split("'")[0])
            except:
                temp_c = None

            # Disk
            disk = psutil.disk_usage('/')
            disk_used = disk.used / (1024 ** 3)  # in GB
            disk_total = disk.total / (1024 ** 3)  # in GB
            disk_percent = disk.percent

            # Uptime
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            uptime_str = str(uptime).split('.')[0]  # Remove microseconds

            info_text = (
                f"CPU Usage: {cpu_percent}% @ {cpu_freq.current:.2f} MHz\n"
                f"RAM Usage: {ram_used:.2f} GB / {ram_total:.2f} GB ({ram_percent}%)\n"
                f"Temperature: {temp_c:.1f} °C\n"
                f"Disk Usage: {disk_used:.2f} GB / {disk_total:.2f} GB ({disk_percent}%)\n"
                f"Uptime: {uptime_str}\n"
            )    

            self.info_label.text = info_text

        except Exception as e:
            self.info_label.text = "Error loading system info: " + str(e)
    
# Main App
class PiTabletApp(App):
    def build(self):
        # Set window size
        Window.size = WINDOW_Size
        Window.clearcolor = (0.1, 0.1, 0.15, 1)

        # Initialize database
        init_database()

        # Screen Manager
        sm = ScreenManager(transition = SlideTransition(duration = 0.3))

        # Add screens
        sm.add_widget(ClockScreen(name = 'clock'))
        sm.add_widget(WeatherScreen(name = 'weather'))
        sm.add_widget(SystemScreen(name = 'system'))
        
        # Swipe detection
        Window.bind(on_touch_down = self.on_touch_down)
        Window.bind(on_touch_up = self.on_touch_up)

        self.touch_start_x = 0
        self.screen_manager = sm

        # Night mode check
        Clock.schedule_interval(self.check_night_mode, 60)

        return sm
    
    def on_touch_down(self, window, touch):
        self.touch_start_x = touch.x

    def on_touch_up(self, window, touch):
        if abs(touch.x - self.touch_start_x) > 100: # Swipe threshold
            screens = ['clock', 'weather', 'system']
            current_index = screens.index(self.screen_manager.current)

            if touch.x < self.touch_start_x: # Swipe left
                next_index = (current_index + 1) % len(screens)
                self.screen_manager.transition.direction = 'left'
            else: # Swipe right
                next_index = (current_index - 1) % len(screens)
                self.screen_manager.transition.direction = 'right'

            self.screen_manager.current = screens[next_index]

    def check_night_mode(self, dt):
        current_hour = datetime.now()
        
        # Night mode
        if NIGHT_MODE_START <= current_hour.hour or current_hour.hour < NIGHT_MODE_END:
            
            pass

if __name__ == '__main__':
    PiTabletApp().run()