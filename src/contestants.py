#!/usr/bin/python
import util
import os
import contestants_index
import contestants_profile
from database_students import database

def run():
    print("Creating contestants")
    util.makedirs("../dist/contestants")
    contestants_index.run()
    for data in database:
        os.makedirs(os.path.normpath("../dist/contestants/" + data["user-id"]), exist_ok=True)
        contestants_profile.run(data["user-id"])


if __name__ == "__main__":
    run()
