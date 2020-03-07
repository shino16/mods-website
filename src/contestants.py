#!/usr/bin/python
import util
import os
import contestants_index
import contestants_profile
from database_students import database

def run():
    print("Creating contestants")
    util.makedirs("../contestants")
    contestants_index.run()
    for data in database:
        os.makedirs(os.path.normpath("../contestants/" + data["name"]), exist_ok=True)
        contestants_profile.run(data["name"])


if __name__ == "__main__":
    run()
