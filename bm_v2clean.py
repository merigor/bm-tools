#! /usr/bin/env python3
"""Convert JSON bookmarks."""
import json
import sys
from pathlib import Path

skiplist = [
    "",
    "lesezeichenleiste",
    "bookmarks menu",
    "^",
    "all bookmarks",
    "bookmarks toolbar",
    "bookmarks_bar",
    "kategorien",
    "aktuelle_nachrichten",
    "importierte lesezeichen",
    "personal toolbar folder",
    "neu und interessant",
    "neu_und_interessant",
    "microsoft websites",
    "microsoft_websites",
    "lenovo_recommended_websites",
]
replacelist = {
    "phd-cs1": "phd-cs",
    "phd-ai1": "phd-ai",
    "phd-hpc1": "phd-hpc",
    "phd-med1": "phd-med",
    "phd-cheminfo1": "phd-cheminfo",
    "phd-00mix": "phd",
    "00unsorted": "links",
    "unsorted": "links",
    "unsorted-ub": "links",
    "_mix": "links",
    "mix": "links",
    "webcenter": "links",
    "1a": "links",
    "eksploit": "security-exploit",
    "haker": "security-hacker",
    "hacker": "security-hacker",
    "brutfors": "security-brute_force",
    "brute force": "security-brute_force",
    "bezopasnost": "security",
    "parol": "security-password",
    "smartfon": "mobile-phone",
    "shifr": "cipher",
    "ochki": "links",
    "js": "dev",
    "python": "dev-py",
    "anb": "links",
    "bag": "security-bug",
    " bag": "security-bug",
    "programmi": "dev-prog",
    "prog": "dev-prog",
    " linux": "linux",
    " .net": "dev-.net",
    "macbook": "hardware-mac",
    "github": "dev",
    "intellekt": "ai_ml",
    "intelligence": "ai_ml",
    "classif": "ai_ml",
    "machine learning": "ai_ml",
    "deep learning": "ai_ml-deep_learning",
    "source code": "dev",
    " cuda": "dev-hpc-cuda",
    "openmp": "dev-hpc-openmp",
    "mpi": "dev-hpc-mpi",
    " mpi": "dev-hpc-mpi",
    "fortran": "dev-fortran",
    "a.i.": "ai_ml",
    "ai": "ai_ml",
    " ai": "ai_ml",
    "aiml": "ai_ml",
    "ssl": "security",
    "secure": "security",
    "encrypt": "security-encryption",
    "beijing": "china-beijing",
    "tablet": "hardware-tablet",
    "c": "dev-c",
    " c": "dev-c",
    " c ": "dev-c",
    " cilk": "dev-cilk",
    "c/c++": "dev-c-c++",
    "c++": "dev-c++",
    "s++": "dev-c++",
    "cxx": "dev-c++",
    "compiler design": "compilers",
    "compiler_design": "compilers",
    "fazzing": "security-fuzzing",
    "trojan": "security-malware",
    "mobil": "mobile-phone",
    "android": "mobile-phone",
    "ios": "links",
    "iphone": "mobile-phone",
    "mozg": "brain",
    "hakaton": "dev",
    "ssd": "hardware-ssd",
    "arduino": "hardware-arduino",
    "raspberry pi": "hardware-raspi",
    "algoritm": "cs-algorithms",
    "algorithm": "cs-algorithms",
    "algodat": "cs-algorithms",
    "algorithms": "cs-algorithms",
    "debian": "linux-debian",
    " iot": "iot",
    "internet of things": "iot",
    "regular expression": "regex",
    "regular expressions": "regex",
    "lit": "literature",
    "literacy": "literature",
    "guitar": "music-guitar",
    "comp": "links",
    "computer": "links",
    "sprachen": "languages",
    "cult": "cultures",
    "persons": "people",
    "sophie": "links",
    "enh": "hpc",
    "opera": "links",
    "webdesign": "web",
    "new_folder": "links",
    "bccn": "bccn-ai_ml",
    "bcan": "bccn-ai_ml",
    "big data": "big_data",
    "bigdata": "big_data",
    "chem": "chemistry",
    "chemie": "chemistry",
    "ubuntu and free software links": "linux-links-ubuntu",
    "ubuntu_and_free_software_links": "linux-links-ubuntu",
    "washing_machine1": "washing_machine",
    "unsorted_tabs": "links",
    "unsorted bookmarks": "links",
    "unlabeled": "links",
    "ultra hd": "hardware-monitor",
    "firefox_and_mozilla_links": "links",
    "database": "databases",
    "deep neural network": "ai_ml-deep_learning",
    "deep speech": "ai_ml-deep_learning",
    "fourier": "fft",
    "google glass": "hardware-augmented_reality",
    "kochen": "health-cooking",
    "cooking": "health-cooking",
    "obuchenie": "courses",
    "online courses": "courses",
    "online_courses": "courses",
    "neuro1": "neuro",
    "os x": "os_x",
    "osx": "os_x",
    "mozilla firefox": "links",
    "mozilla_firefox": "links",
}
devlist = ["prog", "devblog", "developer", "codeproject"]

totaltags = []


def clean_tags(taglist):
    """Clean tags."""
    res = ["links"]
    for i in taglist:
        if i.startswith(" "):
            i = i.strip()
        if i == "":
            continue
        if i.startswith("www") or i.startswith("blog"):
            continue
        if (
            i.endswith(".de")
            or i.endswith(".com")
            or i.endswith(".org")
            or i.endswith(".edu")
            or i.endswith(".ru")
            or i.endswith(".in")
            or i.endswith(".ch")
            or i.endswith(".io")
            or i.endswith(".eu")
            or i.endswith(".uk")
            or i.endswith(".me")
            or i.endswith(".ca")
            or i.endswith(".us")
            or i.endswith(".gov")
            or i.endswith(".fr")
            or i.endswith(".info")
            or i.endswith(".at")
            or i.endswith(".il")
            or i.endswith(".nl")
            or i.endswith(".co")
            or i.endswith(".guru")
            or i.endswith(".cc")
            or i.endswith(".be")
            or i.endswith(".cn")
            or i.endswith(".se")
            or i.endswith(".cz")
            or i.endswith(".dk")
            or i.endswith(".tv")
            or i.endswith(".es")
            or i.endswith(".ro")
            or (i.endswith(".net") and not i == ".net")
        ):
            continue
        tmp = replacelist.get(i, i)
        if tmp in skiplist:
            continue
        if tmp in devlist:
            res.append("dev")
            continue
        if "-" in tmp:
            res += tmp.split("-")
        elif ":" in tmp:
            res += tmp.split(":")
        else:
            res.append(tmp)
    tmp = set(res)
    if len(tmp) > 1 and "links" in tmp:
        tmp.remove("links")
    return list(tmp)


def convert_entries(data):
    """Convert nested arrays to named entries."""
    global totaltags
    res = []
    for i in data:
        entry = {}
        entry["url"] = i
        tags = None
        title = None
        title, tags, entry["date"] = data[i]
        if title is None or title == "":
            title = i
        entry["title"] = title
        entry["tags"] = clean_tags(tags)
        totaltags += entry["tags"]
        res.append(entry)
    return res


if __name__ == "__main__":
    fname = Path(sys.argv[1]).resolve().expanduser()
    with open(fname, "r", encoding="utf-8") as infile:
        ordered = json.load(infile)
    print(f"read: {len(ordered)}")
    entries = convert_entries(ordered)
    print(f"converted: {len(entries)}")
    with open(f"{fname.stem}_v2.json", "w", encoding="utf-8") as outfile:
        json.dump(entries, outfile, indent=4)
    tags = sorted(list(set(totaltags)))
    print(f"tags: {len(tags)}")
    with open("tags.txt", "w", encoding="utf-8") as tagfile:
        tagfile.write("\n".join(tags))
