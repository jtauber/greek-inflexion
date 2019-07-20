#!/usr/bin/env python3

from collections import defaultdict

from pysblgnt import morphgnt_rows

from morphgnt_utils import bcv_tuple

BOOK_NUM = 4


def convert_parse(ccat_parse):
    return ccat_parse[4:7]


NOMINALS = defaultdict(lambda: defaultdict(set))

for row in morphgnt_rows(BOOK_NUM):
    b, c, v = bcv_tuple(row["bcv"])
    if c == 2 and v <= 11:
        if row["ccat-pos"] in ["N-", "A-"]:
            NOMINALS[row["lemma"]][convert_parse(row["ccat-parse"])].add(
                row["norm"] + "  # " + row["robinson"])

for lemma in NOMINALS:
    print("-")
    print("    lemma: {}".format(lemma))
    print("    test_length: false")
    print()
    for parse, form in NOMINALS[lemma].items():
        print("    {}: {}".format(parse, "/".join(form)))
    print()
