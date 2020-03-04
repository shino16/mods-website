#!/usr/bin/python
import util
import contestants_index

def run():
    print("Creating contestants")
    util.makedirs("../contestants")
    contestants_index.run()

if __name__ == "__main__":
    run()
