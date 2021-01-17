#! /usr/bin/env python3
"""Sort bookmarks."""
import json
import sys


def print_results(data):
    print("[")
    for i in sorted(data):
        print("\t{")
        print('\t\t"url":"{}",'.format(i))
        print('\t\t"comments":[{}],'.format(data[i][0]))
        # print(", ".join(list(data[i][0])), end="")
        # print("],")
        print('\t\t"tags":["', end="")
        print('", "'.join(list(data[i][1])), end="")
        print('"],')
        print('\t\t"date":"{}"'.format(data[i][2]))
        print("\t},")
    print("]")


def sort_results(data):
    links = []
    todos = []
    no_http = []
    youtube = []
    for i in data:
        if not i["url"].startswith("http"):
            no_http.append(i)
        elif "youtube.com" in i["url"]:
            youtube.append(i)
        elif "todo" in i["tags"]:
            todos.append(i)
        else:
            links.append(i)
    return (links, todos, no_http, youtube)


def convert_entries(data):
    res = []
    for i in data:
        entry = dict()
        entry["url"] = i
        entry["comment"], entry["tags"], entry["date"] = data[i]
        res.append(entry)
    return res


if __name__ == "__main__":
    with open(sys.argv[1], "r") as infile:
        ordered = json.load(infile)
    entries = convert_entries(ordered)
    # print(len(entries))
    # print(entries[-340])
    # print_results(unsorted)
    # for i in sort_results(unsorted):
    #     with open("{}.json".format(i), "w") as outfile:
    #         json.dump(i.__name__, outfile, indent=4)
    links, todos, no_http, youtube = sort_results(entries)
    print("total: {}".format(len(entries)))
    print("links: {}".format(len(links)))
    print("todos: {}".format(len(todos)))
    print("no_http: {}".format(len(no_http)))
    print("youtube: {}".format(len(youtube)))
    with open("links.json", "w") as outfile:
        json.dump(links, outfile, indent=4)
    with open("todos.json", "w") as outfile:
        json.dump(todos, outfile, indent=4)
    with open("no_http.json", "w") as outfile:
        json.dump(no_http, outfile, indent=4)
    with open("youtube.json", "w") as outfile:
        json.dump(youtube, outfile, indent=4)
