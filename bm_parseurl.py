#! /usr/bin/env python3

if __name__ == "__main__":
    import json
    import sys
    from urllib.parse import urlparse

    with open(sys.argv[1], "r") as infile:
        data = json.load(infile)

        for bm in data:
            try:
                chunks = urlparse(bm)
                data[bm].append(list(chunks))
            except ValueError:
                data[bm].append([])

    with open("test.json", "w+") as outfile:
        json.dump(data, fp=outfile, indent=4)
