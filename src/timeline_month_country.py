#!/usr/bin/python
import sys
import util
import templates
from database_countries import code_to_country
from database_students import month_grouped as s_db_y
from database_timeline import month_indexed as t_db_m
from database_timeline import previous_month
from database_timeline import next_month
from functools import cmp_to_key

def run(month):
    print("Creating timeline/" + month + "/country")
    html = templates.get("timeline/month/country")
    html = templates.initial_replace(html, 1)
    monthdata = t_db_m[month]
    html = html.replace("__MONTH__", month)
    html = html.replace("__NUMBER__", monthdata["number"])
    html = html.replace("__ORDINAL__", util.ordinal(monthdata["number"]))

    if month in previous_month:
        html = html.replace("__PREVIOUS_MONTH__", previous_month[month])
        html = html.replace("__PREVIOUS_MONTH_STYLE__", "")
    else:
        html = html.replace("__PREVIOUS_MONTH_STYLE__", "display: none;")
        html = html.replace("__PREVIOUS_MONTH__", ".") # Google crawler fix

    if month in next_month:
        html = html.replace("__NEXT_MONTH__", next_month[month])
        html = html.replace("__NEXT_MONTH_STYLE__", "")
    else:
        html = html.replace("__NEXT_MONTH_STYLE__", "display: none;")
        html = html.replace("__NEXT_MONTH__", ".") # Google crawler fix

    medals = {}
    if month in s_db_y:
        for row in s_db_y[month]:
            if row["name"] not in medals:
                medals[row["name"]] = {
                    "bestrank": int(row["rank"]),
                    "bestrank>=": "&ge;" if row["rank>="] else "",
                    "gold": 0,
                    "silver": 0,
                    "bronze": 0,
                    "honourable": 0
                    }
            if row["medal"] == "G":
                medals[row["name"]]["gold"] += 1
            elif row["medal"] == "S":
                medals[row["name"]]["silver"] += 1
            elif row["medal"] == "B":
                medals[row["name"]]["bronze"] += 1
            elif row["medal"] == "H":
                medals[row["name"]]["honourable"] += 1

    def keyfn(code):
        m = medals[code]
        return (-m["gold"], -m["silver"], -m["bronze"], -m["honourable"],
                m["bestrank"], code)

    sortedcodes = sorted(medals, key = keyfn)

    tablehtml = ""
    prevcode = ""
    prevrank = 0
    for i, code in enumerate(sortedcodes):
        rowhtml = templates.get("timeline/month/country_row")
        rowhtml = rowhtml.replace("__CODE__", code)
        if prevcode != "" and keyfn(prevcode)[:-1] == keyfn(code)[:-1]:
            rowhtml = rowhtml.replace("__RANK__", prevrank)
        else:
            rowhtml = rowhtml.replace("__RANK__", str(i + 1))
            prevcode = code
            prevrank = str(i + 1)
        rowhtml = rowhtml.replace("__GOLD__", str(medals[code]["gold"]))
        rowhtml = rowhtml.replace("__SILVER__", str(medals[code]["silver"]))
        rowhtml = rowhtml.replace("__BRONZE__", str(medals[code]["bronze"]))
        rowhtml = rowhtml.replace("__HONOURABLE__", str(medals[code]["honourable"]))
        rowhtml = rowhtml.replace("__BEST_RANK__", medals[code]["bestrank>="] + str(medals[code]["bestrank"]))
        tablehtml += rowhtml
    html = html.replace("__TABLE__", tablehtml)

    html = templates.final_replace(html, "../..")
    util.writefile("../timeline/" + month + "/country.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
