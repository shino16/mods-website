#!/usr/bin/python
import csv
from database_countries import code_to_country as c_t_c

database = []
contestant_grouped = {}
month_grouped = {}

with open("database/estudiantes.csv", encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        assert len(row) == 8, "Student row error: {}".format(row)
        entry = {
            "month": row[0],
            "rank": row[1],
            "name": row[2],
            "medal": row[3],
            "website": row[7],
            "rank>=": False
        }
        if entry["medal"] not in ["G", "S", "B", "H", "P"]:
            raise Exception("Student database corrupted! Row: {}".format(row))
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
