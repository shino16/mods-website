#!/usr/bin/python
from distutils.dir_util import copy_tree

def run():
    print("Copying static files")
    copy_tree("./templates/img",  "../dist/img")
    copy_tree("./templates/css",  "../dist/css")

if __name__ == "__main__":
    run()
