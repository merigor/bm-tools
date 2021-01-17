#! /usr/bin/env python3
"""Merge bookmarks."""
import json
import sys
from datetime import datetime
from pathlib import Path


def _get_url(url):
    url = url.strip()
    if url == "":
        return None
    return url


def _get_comment(parts):
    comment = " - ".join(parts).strip()
    return comment


def _get_tags(fname):
    tags = set()
    tag = fname.stem.lower()
    if tag.startswith("links"):
        tags.add("links")
        # data[url][1].add(tag[6:])
    elif tag.startswith("todo"):
        tags.add("todo")
        # data[url][1].add(tag[5:])
    elif tag.startswith("2learn"):
        tags.add("todo")
    elif tag.startswith("mix"):
        tags.add("links")
    elif tag.startswith("backup"):
        tags.add("links")
    elif tag.startswith("merged"):
        tags.add("links")
    elif tag.startswith("result"):
        tags.add("links")
    else:
        tags.add(tag)
    return tags


def _get_ts(fname):
    tmp = fname.stem.lower()
    if tmp.startswith("links"):
        return tmp[6:16]
    if tmp.startswith("todo"):
        return tmp[5:15]
        # ts = tmp[6:]
        # if ts.startswith("2"):
        #     year = ts[0:4]
        #     month = ts[4:6]
        #     day = ts[6:8]
        #     return "{}-{}-{}".format(year, month, day)
    ts = fname.stat().st_mtime
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")


def process_onetab(fname, data):
    with open(fname, "r") as infile:
        for i in infile:
            tmp = i.split("|")
            url = _get_url(tmp[0])
            if url is None:
                continue
            comment = _get_comment(tmp[1:])
            tags = _get_tags(fname)
            ts = _get_ts(fname)
            if url not in data:
                data[url] = [set(), set(), set()]
            data[url][0].add(comment)
            data[url][1].update(tags)
            data[url][2].add(ts)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    unsorted = dict()
    folder = Path(sys.argv[1]).glob("*")
    for f in folder:
        process_onetab(f, unsorted)
    with open("onetab2.json", "w+") as outfile:
        json.dump(unsorted, outfile, sort_keys=True, indent=4, cls=SetEncoder)
