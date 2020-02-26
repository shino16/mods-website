#!/usr/bin/python
import csv
from database_countries import code_to_country as c_t_c

database = []
code_grouped = {}
month_grouped = {}

with open("database/estudiantes.csv", encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        assert len(row) == 9, "Student row error: {}".format(row)
        entry = {
            "month": row[0],
            "rank": row[1],
            "name": row[2],
            "code": row[3],
            "medal": row[4],
            "website": row[8],
            "rank>=": False
        }
        if (entry["medal"] not in ["G", "S", "B", "H", "P"]
                or (entry["code"] != "" and entry["code"] not in c_t_c)):
            raise Exception("Student database corrupted! Row: {}".format(row))
        if entry["rank"][:2] == ">=":
            entry["rank"] = entry["rank"][2:]
            entry["rank>="] = True
        database.append(entry)
        if entry["code"] not in code_grouped:
            code_grouped[entry["code"]] = []
        code_grouped[entry["code"]].append(entry)
        if entry["month"] not in month_grouped:
            month_grouped[entry["month"]] = []
        month_grouped[entry["month"]].append(entry)
