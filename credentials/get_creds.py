### Run script once to authorize you app with oauth and generate pickle file with the given scopes pf permissions.
### Check https://console.cloud.google.com/apis/credentials for details

import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# to grant read/write access to Calendars
scope = ["https://www.googleapis.com/auth/calendar"]
credentialFile = "./client_secret.json"

if __name__ == "__main__":
    if not os.path.exists("token.pickle"):
        flow = InstalledAppFlow.from_client_secrets_file(credentialFile, scope)
        creds = flow.run_console()
        # save the credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
