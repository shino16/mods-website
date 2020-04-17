#!/usr/bin/python
import sys
import util
import templates
from os import path
from database_timeline import month_indexed as timeline
from database_students import contestant_history
from database_students import contestant_grouped

def run(user_id):
    print("Creating contestants/" + user_id + "/index")
    history = contestant_history[user_id]
    html = templates.get("contestants/profile")
    html = templates.initial_replace(html, 2) \
            .replace("__NAME__", contestant_grouped[user_id][0]["name"]) \
            .replace("__GOLD__", str(history["G"])) \
            .replace("__SILVER__", str(history["S"])) \
            .replace("__BRONZE__", str(history["B"])) \
            .replace("__HONOURABLE_MENTION__", str(history["H"])) \
            .replace("__PARTICIPATIONS__", str(sum(history.values())))

    beg, inter, adv, modsmo, special = [""] * 5
    for row in contestant_grouped[user_id]:
        rowhtml = templates.get("contestants/profile_row_" + str(len(row["scores"]))) \
                    .replace("__MONTH__", row["month"]) \
                    .replace("__CONTEST_NAME__", row["contest_name"]) \
                    .replace("__TOTAL_SCORE__", str(row["total_score"])) \
                    .replace("__RANK__", str(row["rank"]))

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

    header4 = templates.get("contestants/profile_table_header_4")
    header6 = templates.get("contestants/profile_table_header_6")
    header_special = templates.get("contestants/profile_table_header_special")
    for code, text, header in (("BEG", beg, header4), ("INT", inter, header4), ("ADV", adv, header4),
                       ("MODSMO", modsmo, header6), ("SPECIAL", special, header_special)):
        if text:
            html = html.replace("__TABLE_HEADER_" + code + "__",
                                header_special if code == "SPECIAL" else header)
            html = html.replace("__TABLE_" + code + "__", text)
        else:
            html = html.replace("__TABLE_HEADER_" + code + "__", "")
            html = html.replace("__TABLE_" + code + "__", "&emsp; No participation yet.")

    html = templates.final_replace(html, "../..")
    util.writefile("../dist/contestants/" + user_id + "/index.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
