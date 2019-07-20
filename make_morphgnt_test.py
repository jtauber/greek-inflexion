#!/usr/bin/env python3

from collections import defaultdict

from pysblgnt import morphgnt_rows

from morphgnt_utils import bcv_tuple, convert_parse


BOOK_NUM = 4


VERBS = defaultdict(lambda: defaultdict(set))

for row in morphgnt_rows(BOOK_NUM):
    b, c, v = bcv_tuple(row["bcv"])
    if c == 2 and v <= 11:
        if row["ccat-pos"] == "V-":
            VERBS[row["lemma"]][convert_parse(row["ccat-parse"])].add(
                row["norm"])

for lemma in VERBS:
    print("-")
    print("    lemma: {}".format(lemma))
    print("    test_length: false")
    print()
    for parse, form in VERBS[lemma].items():
        print("    {}: {}".format(parse, "/".join(form)))
    print()
