#!/usr/bin/python
import sys
import util
import templates
from database_students import id_grouped as s_db_y
from database_timeline import id_indexed as t_db_m
from database_timeline import previous_month
from database_timeline import next_month

def run(id):
    print("Creating timeline/" + id + "/individual")
    html = templates.get("timeline/month/individual")
    html = templates.initial_replace(html, 1)
    monthdata = t_db_m[id]
    html = html.replace("__MONTH__", id)
    html = html.replace("__CONTEST_NAME__", monthdata["name"])
    html = html.replace("__NUMBER__", monthdata["number"])
    html = html.replace("__ORDINAL__", util.ordinal(monthdata["number"]))

    if id in previous_month:
        html = html.replace("__PREVIOUS_MONTH__", previous_month[id])
        html = html.replace("__PREVIOUS_MONTH_STYLE__", "")
    else:
        html = html.replace("__PREVIOUS_MONTH_STYLE__", "display: none;")
        html = html.replace("__PREVIOUS_MONTH__", ".") # Google crawler fix

    if id in next_month:
        html = html.replace("__NEXT_MONTH__", next_month[id])
        html = html.replace("__NEXT_MONTH_STYLE__", "")
    else:
        html = html.replace("__NEXT_MONTH_STYLE__", "display: none;")
        html = html.replace("__NEXT_MONTH__", ".") # Google crawler fix

    tablehtml = ""
    anonymous_found = False
    if id in s_db_y:
        for row in s_db_y[id]:
            rowhtml = templates.get("timeline/month/individual_row_" + str(len(row["scores"])))
            rowhtml = rowhtml.replace("__TOTAL_SCORE__", str(row["total_score"]))
            rowhtml = rowhtml.replace("__RANK__", str(row["rank"]))

            for i, x in enumerate(row["scores"]):
                rowhtml = rowhtml.replace(f"__SCORE_{i+1}__", str(x))

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

            if not monthdata["userinfo_available"]:
                rowhtml = rowhtml.replace("__USERINFO_STYLE__", "display: none;")
            elif row["is_anonymous"]:
                rowhtml = rowhtml.replace("__NAME__", "")
                rowhtml = rowhtml.replace("__USER_ID__", "")
                anonymous_found = True
            else:
                rowhtml = rowhtml.replace("__NAME__", row["name"])
                rowhtml = rowhtml.replace("__USER_ID__", row["user-id"])

            rowhtml = rowhtml.replace("__USERINFO_STYLE__", "")
            tablehtml += rowhtml

    header = ""
    script = ""
    if id in s_db_y and len(s_db_y[id]) >= 1:
        header = templates.get("timeline/month/individual_header_" + str(len(s_db_y[id][0]["scores"])))
        if not monthdata["userinfo_available"]:
            header = header.replace("__USERINFO_STYLE__", "display: none;")
        else:
            header = header.replace("__USERINFO_STYLE__", "")
        script = templates.get("timeline/month/individual_script_" + str(len(s_db_y[id][0]["scores"])))


    html = html.replace("__TABLE__", tablehtml)
    html = html.replace("__TABLE_HEADER__", header)
    html = html.replace("__SORT_SCRIPT__", script)

    html = html.replace("__ANONYMOUS_MSG__",
                        "The names of anonymous contestants are not shown." if anonymous_found else "")

    html = templates.final_replace(html, "../..")
    util.writefile("../dest/timeline/" + id + "/individual.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
