#!/usr/bin/python
import sys
import util
import templates
from os import path
from database_timeline import month_indexed as timeline
from database_students import contestant_history
from database_students import contestant_grouped

def run(name):
    print("Creating contestants/" + name + "/index")
    history = contestant_history[name]
    html = templates.get("contestants/profile")
    html = templates.initial_replace(html, 2) \
            .replace("__NAME__", name) \
            .replace("__GOLD__", str(history["G"])) \
            .replace("__SILVER__", str(history["S"])) \
            .replace("__BRONZE__", str(history["B"])) \
            .replace("__HONOURABLE_MENTION__", str(history["H"])) \
            .replace("__PARTICIPATIONS__", str(sum(history.values())))

    beg, inter, adv, modsmo, special = [""] * 5
    for row in contestant_grouped[name]:
        rowhtml = templates.get("contestants/profile_row") \
                    .replace("__MONTH__", row["month"]) \
                    .replace("__CONTEST_NAME__", row["contest_name"]) \
                    .replace("__SCORE__", row["score"]) \
                    .replace("__RANK__", row["rank"])
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
        if row["contest_name"] == "Beginner":
            beg += rowhtml
        elif row["contest_name"] == "Intermediate":
            inter += rowhtml
        elif row["contest_name"] == "Advanced":
            adv += rowhtml
        elif row["contest_name"] == "MODSMO":
            modsmo += rowhtml
        else:
            special += rowhtml

    header = templates.get("contestants/profile_table_header")
    header_special = templates.get("contestants/profile_table_header_special")
    for code, text in (("BEG", beg), ("INT", inter), ("ADV", adv),
                       ("MODSMO", modsmo), ("SPECIAL", special)):
        if text:
            html = html.replace("__TABLE_HEADER_" + code + "__",
                                header_special if code == "SPECIAL" else header)
            html = html.replace("__TABLE_" + code + "__", text)
        else:
            html = html.replace("__TABLE_HEADER_" + code + "__", "")
            html = html.replace("__TABLE_" + code + "__", "&emsp; No participation yet.")

    html = templates.final_replace(html, "../..")
    util.writefile("../dist/contestants/" + name + "/index.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
