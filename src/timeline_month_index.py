#!/usr/bin/python
import sys
import util
import templates
from math import sqrt
from database_timeline import month_indexed as t_db_m
from database_timeline import previous_month
from database_timeline import next_month
from database_students import month_grouped as contest_results

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

    gold = 0
    silver = 0
    bronze = 0
    honourable = 0
    if month in contest_results:
        for studentdata in contest_results[month]:
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


    if month in contest_results:
        html = html.replace("__INDIVIDUAL_STYLE__", "")
        num_problems = len(contest_results[month][0]["scores"])
        header = templates.get(f"timeline/month/stats/header_{num_problems}")
        count = [[0 for _ in range(8)] for _ in range(num_problems)]
        for entry in contest_results[month]:
            for i, score in enumerate(entry["scores"]):
                count[i][score] += 1
        nums = ""
        for score in range(8):
            rowhtml = templates.get(f"timeline/month/stats/num_{num_problems}")
            rowhtml = rowhtml.replace("__SCORE__", str(score))
            for i in range(num_problems):
                rowhtml = rowhtml.replace(f"__P{i+1}__", str(count[i][score]))
            nums += rowhtml
        means = templates.get(f"timeline/month/stats/index_value_{num_problems}") \
                    .replace("__NAME__", "Mean") \
                    .replace("__STYLE__", "mean")
        maxs = templates.get(f"timeline/month/stats/index_value_{num_problems}") \
                    .replace("__NAME__", "Max") \
                    .replace("__STYLE__", "max")
        sigmas = templates.get(f"timeline/month/stats/index_value_{num_problems}") \
                    .replace("__NAME__", "σ") \
                    .replace("__STYLE__", "sigma")
        for i in range(num_problems):
            total = sum(count[i])
            total_score = sum(score * count[i][score] for score in range(8))
            mean = total_score / total
            means = means.replace(f"__P{i+1}__", "%.3f" % mean)
            max_score = max(score for score in range(8) if count[i][score] or score == 0)
            maxs = maxs.replace(f"__P{i+1}__", str(max_score))
            variance = sum(pow((score - mean), 2) * count[i][score]
                           for score in range(8)) / total
            sigmas = sigmas.replace(f"__P{i+1}__", "%.3f" % sqrt(variance))

        html = html.replace("__STATS_STYLE__", "") \
                   .replace("__TABLE_HEADER__", header) \
                   .replace("__TABLE_NUM__", nums) \
                   .replace("__TABLE_MEAN__", means) \
                   .replace("__TABLE_MAX__", maxs) \
                   .replace("__TABLE_SIGMA__", sigmas)
    else:
        html = html.replace("__INDIVIDUAL_STYLE__", "display: none;")
        html = html.replace("__STATS_STYLE__", "display: none;")


    html = templates.final_replace(html, "../..")
    util.writefile("../dest/timeline/" + month + "/index.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
