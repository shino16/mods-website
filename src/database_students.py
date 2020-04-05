#!/usr/bin/python
import csv
from database_timeline import month_indexed

database = []
contestant_grouped = {}
contestant_history = {}
month_grouped = {}

with open("database/estudiantes.csv", encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        assert len(row) == 6, "Student row error: {}".format(row)
        entry = {
            "month": row[0],
            "rank": row[1],
            "score": row[2],
            "name": row[3],
            "contest_name": month_indexed[row[0]]["name"],
            "medal": row[4],
            "website": row[5],
            "rank>=": False
        }
        if entry["rank"][:2] == ">=":
            entry["rank"] = entry["rank"][2:]
            entry["rank>="] = True
        database.append(entry)
        if entry["name"] not in contestant_grouped:
            contestant_grouped[entry["name"]] = []
        contestant_grouped[entry["name"]].append(entry)
        if entry["month"] not in month_grouped:
            month_grouped[entry["month"]] = []
        month_grouped[entry["month"]].append(entry)

    for contestant, entries in contestant_grouped.items():
        contestant_history[contestant] = {
            "G": 0,
            "S": 0,
            "B": 0,
            "H": 0,
            "P": 0
        }
        for entry in entries:
            contestant_history[contestant][entry["medal"] or "P"] += 1
