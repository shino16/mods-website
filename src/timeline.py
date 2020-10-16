#!/usr/bin/python
import util
import templates
import timeline_index
import timeline_month
from database_timeline import database as t_db

def run():
    print("Creating timeline")
    util.makedirs("../dest/timeline")
    timeline_index.run()
    for monthdata in t_db:
        timeline_month.run(monthdata["id"])

if __name__ == "__main__":
    run()
