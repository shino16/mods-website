#!/usr/bin/python
import sys
import util
import templates
from os import path
from database_timeline import id_indexed as timeline
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
    beg_anon, inter_anon, adv_anon, modsmo_anon, special_anon = [False] * 5
    for row in contestant_grouped[user_id]:
        rowhtml = templates.get("contestants/profile_row_" + str(len(row["scores"]))) \
                    .replace("__MONTH__", row["month"]) \
                    .replace("__CONTEST_NAME__", row["contest_name"]) \
                    .replace("__TOTAL_SCORE__", "" if row["is_anonymous"] else str(row["total_score"])) \
                    .replace("__RANK__", "" if row["is_anonymous"] else str(row["rank"]))

        for i, x in enumerate(row["scores"]):
            rowhtml = rowhtml.replace(f"__SCORE_{i+1}__", "" if row["is_anonymous"] else str(x))

        if not row["is_anonymous"]:
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
        else:
            rowhtml = rowhtml.replace("__MEDAL__", "")
        if row["contest_name"] == "Beginner":
            beg += rowhtml
            beg_anon = beg_anon or row["is_anonymous"]
        elif row["contest_name"] == "Intermediate":
            inter += rowhtml
            inter_anon = inter_anon or row["is_anonymous"]
        elif row["contest_name"] == "Advanced":
            adv += rowhtml
            adv_anon = adv_anon or row["is_anonymous"]
        elif row["contest_name"] == "MODSMO":
            modsmo += rowhtml
            modsmo_anon = modsmo_anon or row["is_anonymous"]
        else:
            special += rowhtml
            special_anon = special_anon or row["is_anonymous"]

    header4 = templates.get("contestants/profile_table_header_4")
    header6 = templates.get("contestants/profile_table_header_6")
    header_special = templates.get("contestants/profile_table_header_special")
    for code, text, anon, header in (
            ("BEG", beg, beg_anon, header4), ("INT", inter, inter_anon, header4),
            ("ADV", adv, adv_anon, header4), ("MODSMO", modsmo, modsmo_anon, header6),
            ("SPECIAL", special, special_anon, header_special)):
        if text:
            html = html.replace("__TABLE_HEADER_" + code + "__",
                                header_special if code == "SPECIAL" else header)
            html = html.replace("__TABLE_" + code + "__", text)
        else:
            html = html.replace("__TABLE_HEADER_" + code + "__", "")
            html = html.replace("__TABLE_" + code + "__", "<dd>No participation yet.</dd>")
        html = html.replace("__ANONYMOUS_MSG_" + code + "__",
                "Results of anonymous participations are hidden." if anon else "")

    html = templates.final_replace(html, "../..")
    util.writefile("../dest/contestants/" + user_id + "/index.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
