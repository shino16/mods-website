#!/usr/bin/python
import sys
import util
import timeline_month_index
import timeline_month_country
import timeline_month_individual

def run(month):
    print("Creating timeline/" + month)
    util.makedirs("../dest/timeline/" + month)
    timeline_month_index.run(month)
    timeline_month_individual.run(month)

if __name__ == "__main__":
    run(sys.argv[1])
