#!/usr/bin/env python3

from collections import defaultdict

from pysblgnt import morphgnt_rows

BOOK_NUM = 4

# @@@ move this to greek-utils

def bcv_tuple(bcv):
    """
    converts a BBCCVV string into a tuple of book, chapter, verse number.

    e.g. "012801" returns (1, 28, 1)
    """
    return (int(i) for i in [bcv[0:2], bcv[2:4], bcv[4:6]])


PARSE_CODES = [
    ('N-', '----DSF-', 'N-DSF'),
    ('A-', '----DSF-', 'A-DSF'),
    ('N-', '----NSM-', 'N-NSM'),
    ('N-', '----DSF-', 'N-PRI'),  # @@@
    ('N-', '----GSF-', 'N-GSF'),
    ('N-', '----NSF-', 'N-NSF'),
    ('N-', '----GSM-', 'N-GSM'),
    ('N-', '----NPM-', 'N-NPM'),
    ('N-', '----ASM-', 'N-ASM'),
    ('N-', '----VSF-', 'N-VSF'),
    ('N-', '----DPM-', 'N-DPM'),
    ('A-', '----NPF-', 'A-NPF'),
    ('N-', '----NPF-', 'N-NPF'),
    ('A-', '----NPF-', 'A-NUI'),  # @@@
    ('A-', '----GPM-', 'A-GPM'),
    ('N-', '----APM-', 'N-APM'),
    ('A-', '----APM-', 'A-NUI'),
    ('A-', '----APM-', 'A-APM'),
    ('N-', '----APF-', 'N-APF'),
    ('N-', '----GSN-', 'N-GSN'),
    ('N-', '----DSM-', 'N-DSM'),
    ('N-', '----ASN-', 'N-ASN'),
    ('A-', '----NSM-', 'A-NSM'),
    ('A-', '----ASN-', 'ADV-S@'),  # @@@
    ('A-', '----ASM-', 'A-ASM'),
    ('A-', '----ASMC', 'A-ASM-C'),  # @@@
    ('N-', '----ASF-', 'N-ASF'),
    ('N-', '----GPN-', 'N-GPN'),
]

def convert_parse(ccat_parse):
    return ccat_parse[4:7]

NOMINALS = defaultdict(lambda: defaultdict(set))

for row in morphgnt_rows(BOOK_NUM):
    b, c, v = bcv_tuple(row["bcv"])
    if c == 2 and v <= 11:
        if row["ccat-pos"] in ["N-", "A-"]:
            assert (row["ccat-pos"], row["ccat-parse"], row["robinson"]) in PARSE_CODES, (row["ccat-pos"], row["ccat-parse"], row["robinson"])
            NOMINALS[row["lemma"]][convert_parse(row["ccat-parse"])].add(row["norm"] + "  # " + row["robinson"])

for lemma in NOMINALS:
    print("-")
    print("    lemma: {}".format(lemma))
    print("    test_length: false")
    print()
    for parse, form in NOMINALS[lemma].items():
        print("    {}: {}".format(parse, "/".join(form)))
    print()
