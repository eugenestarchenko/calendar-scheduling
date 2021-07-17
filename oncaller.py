from sys import exit
from datetime import datetime, timedelta, date
import os.path
import pickle
import click
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import csv_reader
from itertools import cycle, islice
from pprint import pprint


scope = ["https://www.googleapis.com/auth/calendar"]

credentials = None

# default timezone
defaultTimeZone = "America/Los_Angeles"

# your public calendarID
defaultcalendarId = "XXXXXXXX@group.calendar.google.com"

oncall_engineers = csv_reader.rotations
oncall_teams = csv_reader.team_details
oncall_managers = csv_reader.emails

try:
    with open("./credentials/token.pickle", "rb") as token:
        credentials = pickle.load(token)
except:
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
    else:
        print("""Something wrong with creds""")
        raise

service = build("calendar", "v3", credentials=credentials)

# Call G Calendar API
def get_cal_events():
    now = datetime.utcnow().isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId=defaultcalendarId,
            timeMin=now,
            maxResults=30,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming oncall events!")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])

    calendarList = service.calendarList().list().execute()["items"]
    calendar_id = calendarList[0]["id"]

    return events


def get_team(name):
    team_info = csv_reader.team_details
    return team_info[name]


def get_manager_info(name):
    manager_info = csv_reader.emails
    return manager_info[name]


def get_techlead_info(name):
    techlead_info = csv_reader.emails
    return techlead_info[name]


def create_event(
    on_call_rotation_index,
    rotation,
    engineer_info,
    team_info,
    manager_info,
    techlead_info,
    next_monday,
    number_of_eng,
):

    start = next_monday + timedelta(weeks=on_call_rotation_index)
    end = start + timedelta(days=6)
    event = {
        "summary": f"{rotation} Rotation: {engineer_info['name']} ({team_info['emoji']} {team_info['name']} ) ",
        "start": {
            "dateTime": start.strftime("%Y-%m-%dT%H:%M:%M"),
            "timeZone": defaultTimeZone,
        },
        "end": {
            "dateTime": end.strftime("%Y-%m-%dT%H:%M:%M"),
            "timeZone": defaultTimeZone,
        },
        "recurrence": [
            # len of oncall number_of_eng
            f"RRULE:FREQ=WEEKLY;INTERVAL={number_of_eng};COUNT=1"  ### for recurring X-week basis set COUNT=X
        ],
        "attendees": [
            {"email": f"{engineer_info['email']}"},
            {"email": f"{manager_info['email']}"},
            {"email": f"{techlead_info['email']}"},
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    event = (
        service.events()
        .insert(calendarId=defaultcalendarId, body=event, sendNotifications=True)
        .execute()
    )
    print(event)
    print("Event created: %s" % (event.get("htmlLink")))


if __name__ == "__main__":

    print("Checking next 14 oncall events on calendar...")
    if click.confirm("Do you want to continue?", default=False):
        get_cal_events()

    print("Sheduling oncalls rotations on calendar...")
    if click.confirm("Do you want to continue?!", default=True):

        today = datetime.today()
        next_monday = today + timedelta(days=-today.weekday(), weeks=1)

        for rotation in oncall_engineers.keys():
            number_of_eng = len(oncall_engineers[rotation])
            for on_call_rotation_index in oncall_engineers[rotation]:

                engineer_info = oncall_engineers[rotation][on_call_rotation_index]

                team_info = get_team(engineer_info["team"])

                manager_info = get_manager_info(team_info["manager"])

                techlead_info = get_manager_info(team_info["tech lead"])

                print(
                    create_event(
                        on_call_rotation_index,
                        rotation,
                        engineer_info,
                        team_info,
                        manager_info,
                        techlead_info,
                        next_monday,
                        number_of_eng,
                    )
                )
