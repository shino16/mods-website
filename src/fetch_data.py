#!/usr/bin/python
import pickle
import os
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_sheet():
    creds = None
    if os.path.exists('../dest/token.pickle'):
        with open('../dest/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        oauth_path = os.environ["OAUTH_PATH"]
        scope = "https://www.googleapis.com/auth/spreadsheets.readonly"
        flow = InstalledAppFlow.from_client_secrets_file(oauth_path, scope)
        creds = flow.run_local_server(port=0)
        with open("../dest/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)
    return service.spreadsheets()


sheet_id = os.environ["SHEET_ID"]
sheet = get_sheet()


def read_sheet(tab, sheet_range):
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=tab + "!" + sheet_range).execute()
    return [[s.strip() for s in row] for row in result.get("values", [])]
