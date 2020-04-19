#!/usr/bin/python
import re
from fetch_data import read_sheet

database = []
month_indexed = {}
previous_month = {}
diff_indexed = {}
next_month = {}


tab_name = "Metadata"
sheet_range = "A3:BY"


def is_valid(row):
    return bool(row and re.fullmatch(r"\d\d\d\d-\d\d-.+", row[0]))


def parse_contest_name(raw):
    abbr = {"beg": "Beginner", "int": "Intermediate",
            "adv": "Advanced", "modsmo": "MODSMO"}
    return abbr[raw] if raw in abbr else raw.capitalize()


def parse_dates(row):
    def is_date(cell):
        # (uppercase)(lowercase)(lowercase)-(digit)(digit)
        return bool(re.fullmatch(r"[A-Z][a-z][a-z]-\d\d.*", cell))

    dates = [cell[:6] for cell in row if is_date(cell)]
    assert(len(dates) > 0)

    month = dates[0][:3]
    return dates[0][4:] + "–" + dates[-1][4:] + " " + month + " " + row[0][:4]

column_no_participants = 6


prev = None
for i, row in enumerate(filter(is_valid, read_sheet(tab_name, sheet_range))):
    entry = {
        "number": str(i+1),
        "name": parse_contest_name(row[0][8:]),
        "month": row[0][:7],
        "date": parse_dates(row),
        "p_student": row[column_no_participants]
    }
    database.append(entry)
    month_indexed[entry["month"]] = entry
    diff_indexed[entry["name"]] = entry
    if prev:
        previous_month[entry["month"]] = prev
        next_month[prev] = entry["month"]
    prev = entry["month"]
