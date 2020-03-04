#!/usr/bin/python
import util
import templates
from database_students import contestant_grouped as s_db_c
from database_students import contestant_histories as s_db_h

def run():
    print("Creating contestants/index")
    html = templates.get("contestants/index")
    html = templates.initial_replace(html, 2)

    tablehtml = ""
    for contestant, history in s_db_h.items():
        rowhtml = templates.get("contestants/index_row") \
                    .replace("__CONTESTANT__", contestant) \
                    .replace("__GOLD__", str(history["G"])) \
                    .replace("__SILVER__", str(history["S"])) \
                    .replace("__BRONZE__", str(history["B"])) \
                    .replace("__HONOURABLE_MENTION__", str(history["H"])) \
                    .replace("__PARTICIPATIONS__", str(sum(history.values())))
        tablehtml += rowhtml

    html = html.replace("__TABLE__", tablehtml)
    html = templates.final_replace(html, "..")
    util.writefile("../contestants/index.html", html)

if __name__ == "__main__":
    run()