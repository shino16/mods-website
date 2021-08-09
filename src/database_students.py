#!/usr/bin/python
import re
import csv
from database_timeline import id_indexed
from fetch_data import read_sheet


database = []
contestant_grouped = {}
contestant_history = {}
id_grouped = {}


tab_name = ["Contest Database", "MODSMO Database"]
sheet_range = ["A3:P", "A3:S"]
scores_ix = [[8, 9, 10, 11], [9, 10, 11, 12, 13, 14]]
width = [16, 19]
anonymity_ix = [6, 7]


def is_valid(row, index):
    res = row and re.fullmatch(r"\d\d\d\d-\d\d-.+", row[0])
    res = res and (row[0] in id_indexed)
    res = res and re.fullmatch(r"\d+", row[1])
    res = res and re.fullmatch(r".+#\d\d\d\d", row[scores_ix[index][0]-1])

    for i in scores_ix[index]:
        res = res and re.fullmatch(r"\d+", row[i])

    res = res and re.fullmatch(r"\d+", row[scores_ix[index][-1]+1])
    res = res and re.fullmatch(r"\d+", row[scores_ix[index][-1]+2])

    return bool(res)


for index in range(2):
    for row in read_sheet(tab_name[index], sheet_range[index]):
        if not is_valid(row, index):
            continue

        entry = {
            "month": row[0][:7],
            "id": row[0],
            "user-id": row[1],
            "name": row[scores_ix[index][0]-1],
            "scores": [row[i] for i in scores_ix[index]],
            "total_score": row[scores_ix[index][-1]+1],
            "rank": row[scores_ix[index][-1]+2],
            "contest_name": id_indexed[row[0]]["name"],
            "medal": row[-1][0] if len(row) == width[index] else "",
            "is_anonymous": row[anonymity_ix[index]] == "Yes"
        }

        if entry["month"] == "2019-05" and entry["is_anonymous"]:
            continue

        database.append(entry)
        if entry["user-id"] not in contestant_grouped:
            contestant_grouped[entry["user-id"]] = []
        contestant_grouped[entry["user-id"]].append(entry)
        if entry["id"] not in id_grouped:
            id_grouped[entry["id"]] = []
        id_grouped[entry["id"]].append(entry)

    for contestant, entries in contestant_grouped.items():
        contestant_history[contestant] = {
            "G": 0, "S": 0, "B": 0, "H": 0, "P": 0
        }
        for entry in entries:
            contestant_history[contestant][entry["medal"] or "P"] += 1

for _, entries in contestant_grouped.items():
    entries.sort(key=lambda entry: entry["month"], reverse=True)

for id, entries in id_grouped.items():
    if not id.startswith("2019-05") and id_indexed[id]["p_student"] and \
       int(id_indexed[id]["p_student"]) != len(entries):
        raise Exception(f"Number of participants in {id} does not match")
    entries.sort(key=lambda entry: entry["rank"])


for diff in ("Easy", "Hard"):
    id = "GQMO-" + diff
    id_grouped[id] = []
    rank = [0 for _ in range(100)]
    with open(f"../database/GQMO {diff} Exam.csv") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            sz = len(row[:-1])
            entry = {
                "month": "2020",
                "id": id,
                "user-id": "",
                "name": "",
                "scores": row[:-1],
                "total_score": row[-1],
                "contest_name": "GQMO Easy",
                "medal": "",
                "is_anonymous": True
            }
            id_grouped[id].append(entry)
            rank[int(entry["total_score"])] += 1
        for i in range(99, 0, -1):
            rank[i - 1] += rank[i]
        for entry in id_grouped[id]:
            score = int(entry["total_score"])
            entry["rank"] = str(rank[score + 1] + 1)
            entry["percentile"] = "{:.2f}".format((rank[0] - rank[score + 1]) / rank[0] * 100)