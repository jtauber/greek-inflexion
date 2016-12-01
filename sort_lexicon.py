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


for key, lines in sorted(entries.items(), key=lambda i: c.sort_key(i[0])):
    print()
    print(key)
    for line in lines:
        print(line)
