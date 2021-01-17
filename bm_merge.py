#! /usr/bin/env python3


def merge_values(origel, newel):
    titles = sorted(list(set(origel[0] + newel[0])))
    tags = sorted(list(set(origel[1] + newel[1])))
    dates = sorted(list(set(origel[2] + newel[2])))[0]
    return [titles, tags, [dates]]


if __name__ == "__main__":
    import json
    import sys
    from pathlib import Path

    folder = Path(sys.argv[1]).glob("*.json")
    newdict = dict()
    for entry in folder:
        dupl = 0
        print("processing {}".format(entry.name))
        with open(entry, "r") as infile:
            data = json.load(infile)
            for bm in data:
                if bm not in newdict:
                    newdict[bm] = data[bm]
                else:
                    newdict[bm] = merge_values(newdict[bm], data[bm])
                    dupl += 1
            print(
                "read: {} \tduplicates: {} \tnew: {} \ttotal: {}".format(
                    len(data), dupl, len(data) - dupl, len(newdict)
                )
            )
    with open("merged.json", "w+") as outfile:
        outfile.write(json.dumps(newdict, indent=4))
