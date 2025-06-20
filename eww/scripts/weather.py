#!/usr/bin/python3

import requests
from datetime import datetime
import os
import json
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = os.path.expanduser("~/.cache/mywidgets")
ENDPOINT  = "https://api.openweathermap.org/data/2.5/weather"
API_KEY   = os.getenv("WEATHER_API_KEY")

with open(os.path.expanduser("~/.config/eww/scripts/location.txt"), "r") as f:
    LOCATION  = f.readline().strip()

export = {
    "fetch": 0
}

geolocator = Nominatim(user_agent="my_widget")
location   = geolocator.geocode(LOCATION)

try:
    weather = requests.get(ENDPOINT, params={"lat": location.latitude, "lon": location.longitude, "appid": API_KEY, "units": "metric"})
    
    if weather.status_code != 200:
        raise Exception(f"Failed to fetch data: {weather.status_code} {weather.text}")
    
    data = weather.json()
    
    MAIN     = data["weather"][0]["main"]
    ICON     = data["weather"][0]["icon"]
    TEMP     = data["main"]["temp"]
    MIN_TEMP = data["main"]["temp_min"]
    MAX_TEMP = data["main"]["temp_max"]
    HUMIDITY = data["main"]["humidity"]
    WIND     = data["wind"]["speed"]
    SUNRISE  = datetime.fromtimestamp(data["sys"]["sunrise"])
    SUNSET   = datetime.fromtimestamp(data["sys"]["sunset"])
    
    export.update({
        "fetch":    1,
        "main":     MAIN,
        "icon_url": f"https://openweathermap.org/img/wn/{ICON}@2x.png",
        "temp":     int(TEMP),
        "min_temp": int(MIN_TEMP),
        "max_temp": int(MAX_TEMP),
        "humidity": HUMIDITY,
        "wind":     WIND,
        "sunrise":  SUNRISE.strftime("%H:%M"),
        "sunset":   SUNSET.strftime("%H:%M"),
        "location": LOCATION
    })

except Exception as e:
    print(f"Error: {e}")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

with open(os.path.join(CACHE_DIR, "weather.json"), "w") as f:
    json.dump(export, f, indent=4)
    
print("DONE!")
