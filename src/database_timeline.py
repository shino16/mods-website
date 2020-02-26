#!/usr/bin/python
import csv

database = []
month_indexed = {}
code_grouped = {}
previous_month = {}
next_month = {}

with open("database/timeline.csv") as file:
    reader = csv.reader(file)
    prev = ""
    for row in reader:
        assert len(row) == 8, "Timeline row error: {}".format(row)
        entry = {
            "number": row[0],
            "month": row[1],
            "date": row[2],
            "city": row[4],
            "homepage": row[5],
            "p_country": row[6],
            "p_student": row[7]
        }
        if "&" in row[3]:
            entry["code"] = row[3].split("&")[0]
            entry["code2"] = row[3].split("&")[1]
        else:
            entry["code"] = row[3]

        database.append(entry)
        month_indexed[entry["month"]] = entry
        if entry["code"] not in code_grouped:
            code_grouped[entry["code"]] = []
        code_grouped[entry["code"]].append(entry)
        if "code2" in entry:
            if entry["code2"] not in code_grouped:
                code_grouped[entry["code2"]] = []
            code_grouped[entry["code2"]].append(entry)
        if prev != "":
            previous_month[entry["month"]] = prev
            next_month[prev] = entry["month"]
        prev = entry["month"]
