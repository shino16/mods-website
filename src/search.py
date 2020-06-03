#!/usr/bin/python
import util
import templates

def run():
    print("Creating search")
    util.makedirs("../dest/search")
    util.copyfile("templates/search/search.js", "../dest/search/search.js")
    html = templates.get("search/index")
    html = templates.initial_replace(html, 3)
    html = templates.final_replace(html, "..")
    util.writefile("../dest/search/index.html", html)

if __name__ == "__main__":
    run()
