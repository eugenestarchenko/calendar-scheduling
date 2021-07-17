# Google Calendar on-call scheduling

## TLDR

Demo test app. I've learned new things about google calendar api setup, app creation, creds, etc.

Use <https://developers.google.com/calendar/quickstart/> for details
Check for API reference <https://developers.google.com/calendar/v3/reference>
Or <https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.events.html> for details

## ABOUT

Program parses structured text (CSV) of oncall members and generates a set of recurring events on a Google calendar for when each person is oncall.

It consists from 3 python scripts:

- `get_creds.py` generates token based on user credentials to work with your google app scope (create here <https://console.cloud.google.com/apis/credentials/consent?authuser=1&project=calendar-app-XXXX>)
- credentials dir now includes only dummy/empty secrets, so you have to generate your own.

And the app

- `csv_reader.py` parses files in `csv_files` directory
- `oncaller.py` tranforms that data and posts as events into google calendar (defaultcalendarId = "XXXX@group.calendar.google.com"
)

## HOW TO

- Install required dependecies. See `Makefile`
- Generate creds with `get_creds.py`
- Run

```python3
~ python3 oncaller.py 

Extracting data from CSV file for Oncalls
Extracting data from CSV file for Teams
Extracting data from CSV file for Leaders
Checking next 14 oncall events on calendar...
Do you want to continue? [y/N]: y
No upcoming oncall events!
Sheduling oncalls rotations on calendar...
Do you want to continue?! [Y/n]: y
Event created: https://www.google.com/calendar/event?XXXX
```

- Check oncalls on the public calendar <https://calendar.google.com/calendar/embed?XXXXgroup.calendar.google.com>

## TODO (if have more time)

- Processing command-line arguments
- Containarize development build for clean workspace
- Wrap in docker to run cli as a container with ARGS
- Deep dive into google api <https://developers.google.com/calendar/v3/reference/events/instances>
- Test Coverage
- Scheduling as Code to run scheduling  via Pipeline (GithubActions) on cron, maybe
- Rewrite as REST API to make calls to the endpoint (could be API GW + AWS LAMBDA), maybe
- Better code quality (pretty sure =)
- Google Browser Extension?
