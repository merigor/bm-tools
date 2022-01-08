#! /usr/bin/env python3.7

"""
Link title getter.

A program that takes a plain text file with a list of urls (one per line)
as an argument and gets the title of the page.
"""
# import logging
# import os
# import shutil
import sys

# from pathlib import Path
# from urllib import request

# from urllib import parse
# from urllib import error
from requests_html import HTMLSession


if __name__ == "__main__":
    fname = sys.argv[1]
    print(f"Processing: {fname}")
    with open(fname, encoding="utf-8") as infile:
        links = infile.readlines()

    res = []
    session = HTMLSession()
    for i in links:
        url = i.strip()
        if url == "" or url.startswith("chrome") or url.startswith("---"):
            continue
        r = session.get(url)
        if r.status_code != 200:
            print(f"not found: {url}")
            continue
        title = r.html.find("title", first=True)
        if title is not None:
            res.append(f"{url} | {title.text.strip()}")
        else:
            res.append(f"{url} | {url}")

    with open(fname[:-4] + ".ot", "w+") as outfile:
        outfile.write("\n".join(res))
