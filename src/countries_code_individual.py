#!/usr/bin/python
import sys
import util
import templates
from database_countries import code_indexed as c_db_c
from database_countries import previous_code
from database_countries import next_code
from database_students import code_grouped as s_db_c


def run(code):
    print("Creating countries/" + code + "/individual")
    html = templates.get("countries/code/individual")
    html = templates.initial_replace(html, 2)

    html = html.replace("__CODE__", code)
    html = html.replace("__COUNTRY__", c_db_c[code]["country"])

    if code in previous_code:
        html = html.replace("__PREVIOUS_CODE__", previous_code[code])
        html = html.replace("__PREVIOUS_CODE_STYLE__", "")
    else:
        html = html.replace("__PREVIOUS_CODE_STYLE__", "display: none;")
        html = html.replace("__PREVIOUS_CODE__", ".") # Google crawler fix

    if code in next_code:
        html = html.replace("__NEXT_CODE__", next_code[code])
        html = html.replace("__NEXT_CODE_STYLE__", "")
    else:
        html = html.replace("__NEXT_CODE_STYLE__", "display: none;")
        html = html.replace("__NEXT_CODE__", ".") # Google crawler fix

    tablehtml = ""
    if code in s_db_c:
        monthhtml = ""
        lastmonth = ""
        for studentdata in s_db_c[code]:
            rowhtml = templates.get("countries/code/individual_row")
            if studentdata["website"]:
                link = templates.get("timeline/month/individual_student_link")
                link = link.replace("__LINK__", studentdata["website"])
                link = link.replace("__NAME__", studentdata["name"])
                rowhtml = rowhtml.replace("__NAME__", link)
            else:
                rowhtml = rowhtml.replace("__NAME__", studentdata["name"])
            rowhtml = rowhtml.replace("__RANK__", ("&ge;" if studentdata["rank>="] else "") + studentdata["rank"])
            rowhtml = rowhtml.replace("__MONTH__", studentdata["month"])
            if studentdata["medal"] == "G":
                rowhtml = rowhtml.replace("__MEDAL__", templates.get("countries/code/individual_gold"))
            elif studentdata["medal"] == "S":
                rowhtml = rowhtml.replace("__MEDAL__", templates.get("countries/code/individual_silver"))
            elif studentdata["medal"] == "B":
                rowhtml = rowhtml.replace("__MEDAL__", templates.get("countries/code/individual_bronze"))
            elif studentdata["medal"] == "H":
                rowhtml = rowhtml.replace("__MEDAL__", templates.get("countries/code/individual_honourable"))
            else:
                rowhtml = rowhtml.replace("__MEDAL__", "")
            if lastmonth == studentdata["month"]:
                rowhtml = rowhtml.replace("__CLASS__", "")
                monthhtml += rowhtml
            else:
                lastmonth = studentdata["month"]
                # reverse ordered:
                tablehtml = monthhtml + tablehtml
                rowhtml = rowhtml.replace("__CLASS__", "doubleTopLine")
                monthhtml = rowhtml
        # Hacky way of removing first double top line:
        monthhtml = monthhtml.replace("doubleTopLine", "", 1)
        tablehtml = monthhtml + tablehtml

    html = html.replace("__TABLE__", tablehtml)
    html = templates.final_replace(html, "../..")
    util.writefile("../countries/" + code + "/individual.html", html)


if __name__ == "__main__":
    run(sys.argv[1])
