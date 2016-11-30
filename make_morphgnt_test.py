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
    ('-AAPGSM-', 'V-AAP-GSM'),
    ('-PAPNPF-', 'V-PAP-NPF'),
    ('-PMPNPF-', 'V-PNP-NPF'),
    ('-XAPNPM-', 'V-RAP-NPM'),
    ('-XPPASN-', 'V-RPP-ASN'),
    ('2AAD-P--', 'V-AAM-2P'),
    ('2PAD-P--', 'V-PAM-2P'),
    ('2XAI-S--', 'V-RAI-2S'),
    ('3AAI-P--', 'V-AAI-3P'),
    ('3AAI-S--', 'V-AAI-3S'),
    ('3AMI-S--', 'V-2ADI-3S'),  # @@@
    ('3AMI-S--', 'V-ADI-3S'),
    ('3API-S--', 'V-API-3S'),
    ('3APS-P--', 'V-APS-3P'),
    ('3IAI-P--', 'V-IAI-3P'),
    ('3IAI-S--', 'V-IAI-3S'),
    ('3PAI-P--', 'V-PAI-3P'),
    ('3PAI-S--', 'V-PAI-3S'),
    ('3PAS-S--', 'V-PAS-3S'),
    ('3YAI-P--', 'V-LAI-3P'),
    ('3YAI-S--', 'V-LAI-3S'),
]

def convert_parse(ccat_parse):
    if ccat_parse[3] in "DISO":
        result = ccat_parse[1:4] + "." + ccat_parse[0] + ccat_parse[5]
    elif ccat_parse[3] == "P":
        result = ccat_parse[1:4] + "." + ccat_parse[4:7]
    return result

VERBS = defaultdict(lambda: defaultdict(set))

for row in morphgnt_rows(BOOK_NUM):
    b, c, v = bcv_tuple(row["bcv"])
    if c == 2 and v <= 11:
        if row["ccat-pos"] == "V-":
            assert (row["ccat-parse"], row["robinson"]) in PARSE_CODES, (row["ccat-parse"], row["robinson"])
            VERBS[row["lemma"]][convert_parse(row["ccat-parse"])].add(row["norm"])

for lemma in VERBS:
    print("-")
    print("    lemma: {}".format(lemma))
    print("    test_length: false")
    print()
    for parse, form in VERBS[lemma].items():
        print("    {}: {}".format(parse, "/".join(form)))
    print()
