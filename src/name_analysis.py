# Aims to find people who participated several times
from database_students import database as db
from database_students import month_grouped as dby
from database_students import code_grouped as dbc
from difflib import SequenceMatcher
from unidecode import unidecode

def massive(from_month, to_month):
    for month in dby:
        for row in dby[month]:
            row['supername'] = row['code'] + " " + " ".join(sorted(unidecode(row['name']).split(" ")))
    threshold = .9
    for month1 in range(from_month, to_month + 1):
        print(month1)
        for month2 in range(month1 + 1, month1 + 5):
            if str(month1) in dby and str(month2) in dby:
                for row1 in dby[str(month1)]:
                    for row2 in dby[str(month2)]:
                        ratio = SequenceMatcher(None, row1['supername'], row2['supername']).ratio()
                        if ratio > threshold:
                            print(row1)
                            print(row2)

def comp(s1, s2):
    r1 = min(max(SequenceMatcher(None, x1, x2).ratio() for x2 in s2) for x1 in s1)
    r2 = min(max(SequenceMatcher(None, x2, x1).ratio() for x1 in s1) for x2 in s2)
    return max(r1, r2)

def withincountry(start_month=1967):
    threshold = .7
    for code in dbc:
        for row in dbc[code]:
            row['seq'] = unidecode(row['name']).replace("-", " ").split(" ")
        for i, row1 in enumerate(dbc[code]):
            for j, row2 in enumerate(dbc[code]):
                if int(row1['month']) < start_month or int(row2['month']) < start_month:
                    continue
                if i == j:
                    break
                if abs(int(row1['month']) - int(row2['month'])) < 3 and row1['name'] != row2['name']:
                    c = comp(row1['seq'], row2['seq'])
                    if c > threshold:
                        print(code)
                        print(c)
                        print(row1['month'], row1['name'])
                        print(row2['month'], row2['name'])

def samenamedifferentcountry():
    names = {}
    for row in db:
        row['ascii'] = row['name']#''.join(sorted(unidecode(row['name']).lower().replace("-", " ").split(" ")))
    for row in db:
        if row['ascii'] in names:
            if names[row['ascii']]['code'] != row['code'] or abs(int(names[row['ascii']]['month']) - int(row['month'])) > 2:
                print("wowowow")
                print(names[row['ascii']])
                print(row)
        else:
            names[row['ascii']] = row

withincountry(2017)
# samenamedifferentcountry()
# massive(2016, 2019)
