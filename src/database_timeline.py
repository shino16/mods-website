#!/usr/bin/python
import re
from fetch_data import read_sheet

database = []
id_indexed = {}
previous_month = {}
diff_indexed = {}
next_month = {}


tab_name = "Metadata"
sheet_range = "A4:BY"


def is_valid(row):
    return bool(row and re.fullmatch(r"\d\d\d\d-\d\d-.+", row[0]))


def parse_contest_name(raw):
    abbr = {"beg": "Beginner", "int": "Intermediate",
            "adv": "Advanced", "modsmo": "MODSMO"}
    return abbr[raw] if raw in abbr else raw.capitalize()


def parse_dates(row):
    def is_date(cell):
        return bool(re.fullmatch(r"[A-Z][a-z][a-z][a-z]?-\d\d.*", cell))

    dates = [cell[:cell.index(' ')] for cell in row if is_date(cell)]
    if len(dates) == 0:
        return ""

    hyphen = dates[0].index('-')
    month = dates[0][:hyphen]
    return dates[0][hyphen + 1:] + "–" + dates[-1][hyphen + 1:] + " " + month + " " + row[0][:4]

column_no_participants = 6


for i, row in enumerate(filter(is_valid, read_sheet(tab_name, sheet_range))):
    entry = {
        "name": parse_contest_name(row[0][8:]),
        "month": row[0][:7],
        "id": row[0][:7],
        "date": parse_dates(row),
        "p_student": row[column_no_participants],
        "userinfo_available": True,
        "percentile_available": False,
        "notes": "",
    }
    entry["display_name"] = entry["name"]
    entry["timestamp"] = entry["month"] + " " + entry["date"]
    database.append(entry)
    id_indexed[entry["id"]] = entry
    diff_indexed[entry["name"]] = entry


gqmo_easy = {
    "name": "GQMO Easy",
    "display_name": "Global Quarantine Mathematical Olympiad Easy",
    "month": "2020",
    "id": "GQMO-Easy",
    "date": "09–10 May 2020",
    "timestamp": "2020-05 09–10 May 2020e",
    "userinfo_available": False,
    "percentile_available": True,
    "p_student": "254",
    "notes": "Organized by Swiss Maths Olympiad",
}

gqmo_hard = {
    "name": "GQMO Hard",
    "display_name": "Global Quarantine Mathematical Olympiad Hard",
    "month": "2020",
    "id": "GQMO-Hard",
    "date": "16–17 May 2020",
    "timestamp": "2020-05 16",
    "userinfo_available": False,
    "percentile_available": True,
    "p_student": "313",
    "notes": "Organized by Swiss Maths Olympiad",
}

for entry in (gqmo_easy, gqmo_hard):
    database.append(entry)
    id_indexed[entry["id"]] = entry

database.sort(key=lambda entry: entry["timestamp"])

for i, entry in enumerate(database):
    entry["number"] = str(i + 1)


prev = None
for entry in database:
    if prev:
        previous_month[entry["id"]] = prev
        next_month[prev] = entry["id"]
    prev = entry["id"]
