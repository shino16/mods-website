#!/usr/bin/python
import sys
import util
import timeline_month_index
import timeline_month_individual

def run(id):
    print("Creating timeline/" + id)
    util.makedirs("../dest/timeline/" + id)
    timeline_month_index.run(id)
    timeline_month_individual.run(id)

if __name__ == "__main__":
    run(sys.argv[1])
