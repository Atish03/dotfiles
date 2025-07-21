#! /usr/bin/python3

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import json

SCOPES     = ["https://www.googleapis.com/auth/calendar.readonly"]
SCRIPT_DIR = os.path.expanduser("~/.config/eww/scripts/")
CACHE_DIR  = os.path.expanduser("~/.cache/mywidgets")
PRIMARY_ID = "primary"
HOLIDAY_ID = "en.indian#holiday@group.v.calendar.google.com"

service = None

def get_events(calendar_id, max_results=10):
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    return service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute().get('items', [])

def parse_event(event):
    start_str = event['start'].get('dateTime') or event['start'].get('date')

    # try:
    #     dt = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00'))
    # except ValueError:
    #     dt = datetime.datetime.strptime(start_str, "%Y-%m-%d")
    #     dt = dt.replace(tzinfo=datetime.timezone.utc)

    dt = None
    if 'dateTime' in event['start']:
        dt = datetime.datetime.fromisoformat(start_str.replace("Z", "+00:00"))
    else:
        dt = datetime.datetime.strptime(start_str, "%Y-%m-%d")
        dt = dt.replace(tzinfo=datetime.timezone.utc)

    formatted_start = dt.strftime("%d-%m")

    return {
        'summary': event['summary'],
        'start': formatted_start,
        'sort_key': dt
    }

def main():
  try:
      creds = None
      if os.path.exists(os.path.join(SCRIPT_DIR, "secrets/token.json")):
        creds = Credentials.from_authorized_user_file(os.path.join(SCRIPT_DIR, "secrets/token.json"), SCOPES)
      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(
              os.path.join(SCRIPT_DIR, "secrets/calendar.json"), SCOPES
          )
          creds = flow.run_local_server(port=0)
        with open(os.path.join(SCRIPT_DIR, "secrets/token.json"), "w") as token:
          token.write(creds.to_json())
  except Exception as e:
      print(e)

  try:
    global service
    service = build("calendar", "v3", credentials=creds)

    primary_events = get_events(PRIMARY_ID)
    holiday_events = get_events(HOLIDAY_ID)

    combined = [
        parse_event(e) for e in primary_events
    ] + [
        parse_event(e) for e in holiday_events
    ]

    combined.sort(key=lambda x: x['sort_key'])
    next_five = list(map(lambda x: {"start": x["start"], "summary": x["summary"]}, combined[:5]))

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    with open(os.path.join(CACHE_DIR, "calendar.json"), "w") as f:
        json.dump(next_five, f, indent=4)
        
    print("DONE!")

  except Exception as e:
      print(e)


if __name__ == "__main__":
  main()
