#! /usr/bin/env python3
"""Convert chrome JSON bookmarks into a flat JSON file."""
import datetime
import json
import sys
import time
from pathlib import Path


def _get_ts(dt):
    microseconds = int(dt, 16) / 10
    seconds, microseconds = divmod(microseconds, 1000000)
    days, seconds = divmod(seconds, 86400)

    return datetime.datetime(1601, 1, 1) + datetime.timedelta(
        days, seconds, microseconds
    )


def convert_date(datestr):
    """Convert epoch in us into date string."""
    date = float(datestr)
    if len(datestr) == 16:
        date /= 1000000
    elif len(datestr) == 13:
        date /= 1000
    return time.strftime("%Y-%m-%d", time.localtime(date))


def process_chrome(obj, result, taglist):
    if isinstance(obj, dict):
        if "url" in obj or "uri" in obj:
            url = obj.get("url", obj.get("uri", "")).strip()
            if url not in result:
                result[url] = [set(), set(), set()]
            comment = obj.get("name", None)
            if comment is None:
                comment = obj.get("title", "")
            date = obj.get("date_added", None)
            if date is None:
                date = obj.get("dateAdded", 0)
                if date is None:
                    print(obj)
            # ts = _get_ts(hex(int(date) * 10)[2:17]).strftime("%Y-%m-%d")
            ts = convert_date(str(date))
            result[url][0].add(comment)
            result[url][1].update(taglist)
            result[url][2].add(ts)
        if "children" in obj:
            tmp = obj.get("name", None)
            if tmp is None:
                tmp = obj.get("title", "")
            tmp = tmp.lower()
            if tmp in ["bookmark bar", "bookmarks bar"]:
                process_chrome(obj["children"], result, taglist)
            else:
                process_chrome(obj["children"], result, taglist + [tmp])
        if "roots" in obj:
            process_chrome(obj["roots"], result, taglist)
        if "bookmark_bar" in obj:
            process_chrome(obj["bookmark_bar"], result, taglist)
    elif isinstance(obj, list):
        for i in obj:
            process_chrome(i, result, taglist)
    else:
        # print("\t" * offset, obj)
        pass

    # print(
    #     format(
    #         _get_ts(hex(13024882639633631 * 10)[2:17]),
    #         "%a, %d %B %Y %H:%M:%S %Z",
    #     )
    # )


def process_folder(dirname, unsorted):
    folder = Path(dirname).glob("*")
    for f in folder:
        name = f.resolve().expanduser()
        print("processing {}".format(name))
        if name.is_dir():
            # print("is dir")
            process_folder(name, unsorted)
        elif name.is_file():
            # print("is file")
            try:
                with open(name, "r") as infile:
                    data = json.load(infile)
                    process_chrome(data, unsorted, ["links"])
            except json.decoder.JSONDecodeError:
                print("json decode error: {}".format(name))
        else:
            print("unknown: {}".format(name))


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    unsorted = dict()
    process_folder(sys.argv[1], unsorted)
    with open("chrome.json", "w") as outfile:
        json.dump(unsorted, outfile, sort_keys=True, indent=4, cls=SetEncoder)
