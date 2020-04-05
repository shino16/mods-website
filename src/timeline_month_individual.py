#!/usr/bin/python
import sys
import util
import templates
from database_countries import code_to_country
from database_students import month_grouped as s_db_y
from database_timeline import month_indexed as t_db_m
from database_timeline import previous_month
from database_timeline import next_month

def run(month):
    print("Creating timeline/" + month + "/individual")
    html = templates.get("timeline/month/individual")
    html = templates.initial_replace(html, 1)
    monthdata = t_db_m[month]
    html = html.replace("__MONTH__", month)
    html = html.replace("__CONTEST_NAME__", monthdata["name"])
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

    tablehtml = ""
    if month in s_db_y:
        for row in s_db_y[month]:
            rowhtml = templates.get("timeline/month/individual_row")
            rowhtml = rowhtml.replace("__NAME__", row["name"])
            rowhtml = rowhtml.replace("__USER_ID__", row["user-id"])
            rowhtml = rowhtml.replace("__RANK__", ("&ge;" if row["rank>="] else "") + row["rank"])
            rowhtml = rowhtml.replace("__SCORE__", row["score"])
            if row["medal"] == "G":
                rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/month/individual_gold"))
            elif row["medal"] == "S":
                rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/month/individual_silver"))
            elif row["medal"] == "B":
                rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/month/individual_bronze"))
            elif row["medal"] == "H":
                rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/month/individual_honourable"))
            else:
                rowhtml = rowhtml.replace("__MEDAL__", "")
            tablehtml += rowhtml
    html = html.replace("__TABLE__", tablehtml)

    html = templates.final_replace(html, "../..")
    util.writefile("../timeline/" + month + "/individual.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
