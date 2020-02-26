#!/usr/bin/python
import csv

database = []
month_indexed = {}
previous_month = {}
next_month = {}

with open("database/timeline.csv") as file:
    reader = csv.reader(file)
    prev = ""
    for row in reader:
        assert len(row) == 6, "Timeline row error: {}".format(row)
        entry = {
            "number": row[0],
            "month": row[1],
            "date": row[2],
            "homepage": row[3],
            "p_country": row[4],
            "p_student": row[5]
        }
        database.append(entry)
        month_indexed[entry["month"]] = entry
        if prev != "":
            previous_month[entry["month"]] = prev
            next_month[prev] = entry["month"]
        prev = entry["month"]
