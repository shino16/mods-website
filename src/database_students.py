#!/usr/bin/python
import pickle
import csv
import os
import re
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from database_timeline import month_indexed


database = []
contestant_grouped = {}
contestant_history = {}
month_grouped = {}


scope = "https://www.googleapis.com/auth/spreadsheets.readonly"
sheet_id = os.environ["SHEET_ID"]
oauth_path = os.environ["OAUTH_PATH"]
tab_name = ["Contest Database", "MODSMO Database"]
sheet_range = ["A3:Q", "A3:T"]
scores_ix = [[9, 10, 11, 12], [10, 11, 12, 13, 14, 15]]
width = [17, 20]


def get_sheet():
    creds = None
    if os.path.exists('../dest/token.pickle'):
        with open('../dest/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(oauth_path, scope)
        creds = flow.run_local_server(port=0)
        with open("../dest/token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)
    return service.spreadsheets()


def read_sheet(index, sheet):
    result = sheet.values().get(
        spreadsheetId=sheet_id,
        range=tab_name[index] + "!" + sheet_range[index]).execute()

    return result.get("values", [])


def is_valid(row, index):
    res = re.fullmatch(r"\d\d\d\d-\d\d-.+", row[0])
    res = res and (row[0][0:7] in month_indexed)
    res = res and re.fullmatch(r".+#....", row[scores_ix[index][0]-1])
    res = res and re.fullmatch(r"\d+", row[1])

    for i in scores_ix[index]:
        res = res and re.fullmatch(r"\d+", row[i])

    res = res and re.fullmatch(r"\d+", row[scores_ix[index][-1]+1])
    res = res and re.fullmatch(r"\d+", row[scores_ix[index][-1]+2])

    return bool(res)


sheet = get_sheet()
for index in range(2):
    for row in read_sheet(index, sheet):
        if not is_valid(row, index):
            continue

        entry = {
            "month": row[0][0:7],
            "user-id": row[1],
            "name": row[scores_ix[index][0]-1],
            "scores": [int(row[i]) for i in scores_ix[index]],
            "total_score": int(row[scores_ix[index][-1]+1]),
            "rank": int(row[scores_ix[index][-1]+2]),
            "contest_name": month_indexed[row[0][0:7]]["name"],
            "medal": row[-1][0] if len(row) == width[index] else ""
        }
        database.append(entry)
        if entry["user-id"] not in contestant_grouped:
            contestant_grouped[entry["user-id"]] = []
        contestant_grouped[entry["user-id"]].append(entry)
        if entry["month"] not in month_grouped:
            month_grouped[entry["month"]] = []
        month_grouped[entry["month"]].append(entry)

    for contestant, entries in contestant_grouped.items():
        contestant_history[contestant] = {
            "G": 0, "S": 0, "B": 0, "H": 0, "P": 0
        }
        for entry in entries:
            contestant_history[contestant][entry["medal"] or "P"] += 1

for _, entries in contestant_grouped.items():
    entries.sort(key=lambda entry: entry["month"], reverse=True)

for _, entries in month_grouped.items():
    entries.sort(key=lambda entry: entry["rank"])