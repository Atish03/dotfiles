#!/usr/bin/python3

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR    = os.path.expanduser("~/.cache/mywidgets")
FORMULA_API  = "https://api.formula1.com/v1/event-tracker"
API_KEY      = os.getenv("F1_API_KEY")

export = {
    "fetch"   : 0,
    "country" : None,
    "location": None,
    "winners" : []
}

def get_best_text_color(bg_color):
    r = int(bg_color[0:2], 16)
    g = int(bg_color[2:4], 16)
    b = int(bg_color[4:6], 16)
    
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    
    if luminance > 0.5:
        return "#4A4A4A"
    else:
        return "#FFFFFF"

try:
    event = requests.get(FORMULA_API, headers={"apiKey": API_KEY, "locale": "en"})
    if event.status_code != 200:
        raise Exception(f"{event.json()}")
    
    event_details = event.json()
    race_results  = event_details["raceResults"]
    meeting_info  = event_details["race"]

    export.update({
        "fetch"        : 1,
        "upcoming"     : True if len(race_results) == 0 else False,
        "country"      : meeting_info["meetingCountryName"],
        "location"     : meeting_info["meetingLocation"],
        "meeting_start": datetime.fromisoformat(meeting_info["meetingStartDate"][:-1] + "+00:00").strftime("%d-%m-%Y %H:%M"),
    })

    for position in race_results: 
        driver    = position["driverTLA"]
        race_time = position["raceTime"]
        color     = position["teamColourCode"]
        team      = position["teamName"]
        
        export["winners"].append({
            "driver"    : driver,
            "race_time" : race_time,
            "color"     : f"#{str.upper(color)}",
            "text_color": get_best_text_color(color),
            "team"      : team
        })
        
except Exception as e:
    print(f"Error fetching data from API: {e}")

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

with open(os.path.join(CACHE_DIR, "event.json"), "w") as f:
    json.dump(export, f, indent=4)
    
print("DONE!")
