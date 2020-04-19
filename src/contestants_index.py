#!/usr/bin/python
import util
import templates
from database_students import contestant_grouped as s_db_c
from database_students import contestant_history as s_db_h

def run():
    print("Creating contestants/index")
    html = templates.get("contestants/index")
    html = templates.initial_replace(html, 2)

    tablehtml = ""
    print(s_db_h.items())
    sorted_items = sorted(s_db_h.items(), reverse=True, key=lambda item: ("%02d" * 5) % (item[1]["G"], item[1]["S"], item[1]["B"], item[1]["H"], sum(item[1].values())))
    for contestant, history in sorted_items:
        rowhtml = templates.get("contestants/index_row") \
                    .replace("__NAME__", s_db_c[contestant][0]["name"]) \
                    .replace("__USER_ID__", contestant) \
                    .replace("__GOLD__", str(history["G"])) \
                    .replace("__SILVER__", str(history["S"])) \
                    .replace("__BRONZE__", str(history["B"])) \
                    .replace("__HONOURABLE_MENTION__", str(history["H"])) \
                    .replace("__PARTICIPATIONS__", str(sum(history.values())))
        tablehtml += rowhtml

    html = html.replace("__TABLE__", tablehtml)
    html = templates.final_replace(html, "..")
    util.writefile("../dest/contestants/index.html", html)

if __name__ == "__main__":
    run()