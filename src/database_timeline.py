#!/usr/bin/python
import csv

database = []
month_indexed = {}
previous_month = {}
diff_indexed = {}
next_month = {}

with open("../database/timeline.csv") as file:
    reader = csv.reader(file)
    prev = ""
    for i, row in enumerate(reader):
        assert len(row) == 5, "Timeline row error: {}".format(row)
        entry = {
            "number": str(i+1),
            "name": row[0],
            "month": row[1],
            "date": row[2],
            "homepage": row[3],
            "p_student": row[4]
        }
        database.append(entry)
        month_indexed[entry["month"]] = entry
        diff_indexed[entry["name"]] = entry
        if prev != "":
            previous_month[entry["month"]] = prev
            next_month[prev] = entry["month"]
        prev = entry["month"]
