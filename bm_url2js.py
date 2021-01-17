#! /usr/bin/env python3
"""Convert *.url bookmarks to JSON."""
import codecs
import json
import sys
from datetime import datetime
from pathlib import Path


def _get_url(data, fname):
    found = False
    url = None
    for i in data:
        if i.startswith("URL="):
            tmp = i[4:].strip()
            if found:
                if tmp != url:
                    print("multiple entries in {}".format(fname))
                    print(tmp)
                    print(url)
            else:
                found = True
                url = tmp
    if not found:
        print("no url in {}".format(fname))
    return url


def _get_comment(fname):
    return fname.stem


def _get_ts(fname):
    ts = fname.stat().st_mtime
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")


def process_url(fname, data):
    lines = []
    try:
        with codecs.open(fname, "r", "cp1251") as infile:
            for i in infile:
                lines.append(i)
    except UnicodeDecodeError:
        print("decode error: {}".format(fname))
    url = _get_url(lines, fname)
    if url is None:
        return
    comment = _get_comment(fname)
    tags = "links"
    ts = _get_ts(fname)
    if url not in data:
        data[url] = [set(), set(), set()]
    data[url][0].add(comment)
    data[url][1].add(tags)
    data[url][2].add(ts)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def process_folder(dirname, unsorted):
    folder = Path(dirname).glob("*")
    for f in folder:
        name = f.resolve().expanduser()
        # print("processing {}".format(name))
        if name.is_dir():
            # print("is dir")
            process_folder(name, unsorted)
        elif name.is_file():
            # print("is file")
            process_url(name, unsorted)
        else:
            print("unknown: {}".format(name))


if __name__ == "__main__":
    unsorted = dict()
    process_folder(sys.argv[1], unsorted)
    with open("url.json", "w") as outfile:
        json.dump(unsorted, outfile, sort_keys=True, indent=4, cls=SetEncoder)
