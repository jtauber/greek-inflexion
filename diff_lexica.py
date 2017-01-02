#!/usr/bin/env python3

import yaml


with open("morphgnt_lexicon.yaml") as f:
    lexicon1 = yaml.load(f)

with open("lxx_lexicon.yaml") as f:
    lexicon2 = yaml.load(f)

in_both = set()
in_1_only = set()
in_2_only = set()

for key in lexicon1:
    if key in lexicon2:
        in_both.add(key)
    else:
        in_1_only.add(key)

for key in lexicon2:
    if key in lexicon1:
        assert key in in_both
    else:
        in_2_only.add(key)

print("both", len(in_both))
print("1 only", len(in_1_only))
print("2 only", len(in_2_only))

PARTS = [
    "1-", "1+", "2-", "3-", "3+",
    "4-", "4+", "5-", "5+",
    "6-", "6+", "7-", "8-",
]

match = 0
mismatch = 0
none_1 = 0
none_2 = 0

for key in in_both:
    for part in PARTS:
        value1 = lexicon1[key].get("stems", {}).get(part)
        value2 = lexicon2[key].get("stems", {}).get(part)

        if value1 != value2:
            if value1 is None:
                none_1 += 1
            elif value2 is None:
                none_2 += 1
            else:
                mismatch += 1
                print(key, part, value1, value2)
        else:
            match += 1

print(
    match, "match;",
    none_1, "none1;",
    none_2, "none2;",
    mismatch, "mismatch"
)
