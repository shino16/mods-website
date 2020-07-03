#!/usr/bin/python
from distutils.dir_util import copy_tree
from database_students import database as s_db
from database_timeline import database as t_db

def run():
    def enc(x):
        if isinstance(x, list):
            return "-".join(map(str, x))
        else:
            return str(x)

    print("Copying static files")
    copy_tree("./templates/img",  "../dest/img")
    copy_tree("./templates/css",  "../dest/css")
    with open("../dest/search/students.csv", "w", encoding="utf8") as f:
        for entry in s_db:
            f.write(",".join(map(enc, entry.values())))
            f.write("\n")
    with open("../dest/search/timeline.csv", "w", encoding="utf8") as f:
        for entry in t_db:
            f.write(",".join(map(enc, entry.values())))
            f.write("\n")
    with open("../dest/CNAME", "w", encoding="utf8") as f:
        f.write("mathematics.isodn.org")

if __name__ == "__main__":
    run()
