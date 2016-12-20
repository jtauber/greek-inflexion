#!/usr/bin/env python3

from collections import defaultdict
import sys

from pyuca import Collator
c = Collator()


filename = sys.argv[1]

entries = defaultdict(list)

key = None

with open(filename) as f:
    for line in f:
        if line.strip() == "":
            continue
        elif line.startswith("    "):
            assert key
            entries[key].append(line.rstrip())
        else:
            key = line.strip()


def sort_key(i):
    key = i[0]
    if "++" in key:
        left_key = key.split("++")[1].split(":")[0]
        middle_key = key.split("++")[0]
    else:
        left_key = key.split(":")[0]
        middle_key = " "

    return (c.sort_key(left_key), c.sort_key(middle_key), c.sort_key(key))


for key, lines in sorted(entries.items(), key=sort_key):
    print()
    print(key)
    for line in lines:
        print(line)
