#!/usr/bin/python
import config
import templates
import util
from database_timeline import database as t_db

def run():
    print("Creating timeline/index")
    html = templates.get("timeline/index")
    html = templates.initial_replace(html, 1)

    tablehtml = ""
    for row in t_db:
        rowhtml = templates.get("timeline/index_row")
        rowhtml = rowhtml.replace("__NUMBER__", row["number"])
        rowhtml = rowhtml.replace("__MONTH__", row["month"])
        rowhtml = rowhtml.replace("__ID__", row["id"])
        rowhtml = rowhtml.replace("__CONTEST_NAME__", row["name"])
        rowhtml = rowhtml.replace("__DATE__", row["date"])
        rowhtml = rowhtml.replace("__TIMESTAMP__", row["timestamp"])
        rowhtml = rowhtml.replace("__P_STUDENT__", row["p_student"])
        rowhtml = rowhtml.replace("__NOTES__", row["notes"])
        tablehtml = rowhtml + tablehtml
    html = html.replace("__TABLE__", tablehtml)

    html = templates.final_replace(html, "..")
    util.writefile("../dest/timeline/index.html", html)

if __name__ == "__main__":
    run()
