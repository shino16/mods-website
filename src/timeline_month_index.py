#!/usr/bin/python
import sys
import util
import templates
from database_timeline import month_indexed as t_db_m
from database_timeline import previous_month
from database_timeline import next_month
from database_students import month_grouped as s_db_y

def run(month):
    print("Creating timeline/" + month + "/index")
    html = templates.get("timeline/month/index")
    html = templates.initial_replace(html, 1)
    monthdata = t_db_m[month]
    html = html.replace("__MONTH__", month)
    html = html.replace("__CONTEST_NAME__", monthdata["name"])
    html = html.replace("__NUMBER__", monthdata["number"])
    html = html.replace("__ORDINAL__", util.ordinal(monthdata["number"]))
    html = html.replace("__DATE__", monthdata["date"])


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

    if monthdata["p_student"] != "":
        html = html.replace("__P_STUDENT_STYLE__", "")
        html = html.replace("__P_STUDENT__", monthdata["p_student"])
    else:
        html = html.replace("__P_STUDENT_STYLE__", "display: none;")

    if monthdata["homepage"] != "":
        html = html.replace("__HOMEPAGE_STYLE__", "")
        html = html.replace("__HOMEPAGE__", monthdata["homepage"])
    else:
        html = html.replace("__HOMEPAGE_STYLE__", "display: none;")
        html = html.replace("__HOMEPAGE__", ".") # Google crawler fix

    gold = 0
    silver = 0
    bronze = 0
    honourable = 0
    if month in s_db_y:
        for studentdata in s_db_y[month]:
            if studentdata["medal"] == "G":
                gold += 1
            elif studentdata["medal"] == "S":
                silver += 1
            elif studentdata["medal"] == "B":
                bronze += 1
            elif studentdata["medal"] == "H":
                honourable += 1
        html = html.replace("__AWARDS_STYLE__", "")
        html = html.replace("__GOLD__", str(gold))
        html = html.replace("__SILVER__", str(silver))
        html = html.replace("__BRONZE__", str(bronze))
        html = html.replace("__HONOURABLE__", str(honourable))
    else:
        html = html.replace("__AWARDS_STYLE__", "display: none;")

    html = templates.final_replace(html, "../..")
    util.writefile("../dist/timeline/" + month + "/index.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
