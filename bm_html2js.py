#! /usr/bin/env python3
"""Convert netscape bookmarks file to JSON."""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

from bs4 import BeautifulSoup

# import json
# from datetime import datetime
# from pathlib import Path


# class MyHTMLParser(HTMLParser):
#     correct = False
#     href = False
#     tag = False
#     links = dict()
#     tags = []

#     def handle_decl(self, decl: str) -> None:
#         if decl != "DOCTYPE NETSCAPE-Bookmark-file-1":
#             self.correct = True

#     def handle_starttag(self, tag, attrs):
#         # print("Encountered a start tag:", tag)
#         if tag == "h3":
#             self.tag = True
#         for a in attrs:
#             if a[0] == "href":
#                 print(a[1], end=" ")
#                 self.href = True
#             elif a[0] == "add_time":
#                 print(
#                     datetime.utcfromtimestamp(int(a[1])).strftime("%Y-%m-%d")
#                 )
#             elif a[0] == "last_modified":
#                 print(
#                     datetime.utcfromtimestamp(int(a[1])).strftime("%Y-%m-%d")
#                 )

#     def handle_endtag(self, tag):
#         # print("Encountered an end tag :", tag)
#         if tag == "dl":
#             self.tags = self.tags[:-1]

#     def handle_data(self, data):
#         if self.href:
#             print("| " + data)
#             print("\t" + ", ".join(self.tags))
#             self.href = False
#         elif self.tag:
#             self.tags.append(data)
#             self.tag = False


# def _get_comment(fname):
#     return fname.stem


# def _get_ts(fname):
#     ts = fname.stat().st_mtime
#     return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")


# def process_html(fname, unsorted):
#     print(fname)
#     with open(fname, "r") as infile:
#         data = infile.readlines()
#     parser = MyHTMLParser()
#     parser.feed("".join(data))
#     if not parser.correct:
#         print("File is not in correct (Netscape) format ...")
#         return


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


# def process_folder(dirname, unsorted):
#     folder = Path(dirname).glob("*")
#     for f in folder:
#         name = f.resolve().expanduser()
#         # print("processing {}".format(name))
#         if name.is_dir():
#             # print("is dir")
#             process_folder(name, unsorted)
#         elif name.is_file():
#             # print("is file")
#             process_html(name, unsorted)
#         else:
#             print("unknown: {}".format(name))


def convert_date(datestr):
    """Convert epoch in us into date string."""
    date = float(datestr)
    if len(datestr) == 16:
        date /= 1000000
    elif len(datestr) == 13:
        date /= 1000
    return time.strftime("%Y-%m-%d", time.localtime(date))


def standardize_tag(tag):
    """Convert tag to a uniform string."""
    return tag.lower().replace(" ", "_")


def get_tags_date(link, default_date=None):
    """Extract tags and date from the link."""
    tags = ["links"]
    date = ""
    fltr = [
        "Bookmarks Menu",
        "Bookmark Bar",
        "Personal Toolbar Folder",
        "Importierte Lesezeichen",
        "Bookmarks Toolbar",
        "Kein Label vorhanden",
        "Unsorted Bookmarks",
        "Unsortierte Lesezeichen",
        "Recently Bookmarked",
        "Recent Tags",
    ]
    for parent in link.parents:
        if parent.name == "dl":
            for sibling in parent.previous_siblings:
                if sibling.name == "h3":
                    tags += sibling.get_text().split(">")
                    datestr = (
                        sibling.get("add_date", None)
                        or sibling.get("last_visit", None)
                        or sibling.get("last_modified", None)
                        or default_date
                    )
                    date = convert_date(datestr)
            for sibling in parent.next_siblings:
                if sibling.name == "h3":
                    tags += sibling.get_text().split(">")
                    datestr = (
                        sibling.get("add_date", None)
                        or sibling.get("last_visit", None)
                        or sibling.get("last_modified", None)
                        or default_date
                    )
                    date = convert_date(datestr)
            break
    return ([standardize_tag(i) for i in tags if i not in fltr], date)


def process_html(data, result, default_date=None):
    """Parse HTML."""
    html = BeautifulSoup(data, "html.parser")
    for link in html.find_all("a"):
        url = link["href"]
        if url in ["", "about:blank"]:
            continue
        comment = link.get_text()
        tags, date = get_tags_date(link, default_date)
        if url not in result:
            result[url] = [[comment], tags, [date]]
        else:
            comments = sorted(list(set(result[url][0] + [comment])))
            tags = sorted(list(set(result[url][1] + tags)))
            date = sorted(list(set(result[url][2] + [date])))[0]
            result[url] = [comments, tags, [date]]
        # print("{} | {}".format(link["href"], link.get_text()))
        # print(get_tags_date(link))
        # for parent in link.parents:
        #     print(parent.name)
        # print(link.parent.get_text().split("&gt;"))
        # print()


if __name__ == "__main__":
    unsorted = dict()
    folder = Path(sys.argv[1]).glob("*")
    for f in folder:
        filedate = str(f.stat().st_ctime)
        with open(f, "r") as infile:
            data = infile.readlines()
        process_html("\n".join(data), unsorted, default_date=filedate)

    with open(
        "html-{}.json".format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S")),
        "w",
    ) as outfile:
        json.dump(unsorted, outfile, sort_keys=True, indent=4, cls=SetEncoder)
