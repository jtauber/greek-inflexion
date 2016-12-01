#!/usr/bin/env python3

from collections import defaultdict

from pysblgnt import morphgnt_rows

from accent import strip_length
from greek_inflexion import GreekInflexion


ginflexion = GreekInflexion(
    "stemming.yaml",
    "morphgnt_johannine_lexicon.yaml",
    strip_length=True
)


# @@@ move this to greek-utils

def bcv_tuple(bcv):
    """
    converts a BBCCVV string into a tuple of book, chapter, verse number.

    e.g. "012801" returns (1, 28, 1)
    """
    return (int(i) for i in [bcv[0:2], bcv[2:4], bcv[4:6]])


def convert_parse(ccat_parse):
    if ccat_parse[3] in "DISO":
        result = ccat_parse[1:4] + "." + ccat_parse[0] + ccat_parse[5]
    elif ccat_parse[3] == "P":
        result = ccat_parse[1:4] + "." + ccat_parse[4:7]
    elif ccat_parse[3] == "N":
        result = ccat_parse[1:4]
    if result[1] == "P" and result[0] not in "AF":
        result = result[0] + "M" + result[2:]
    return result


PARTS = {
    "1-": [
        "PAD", "PAI", "PAN", "PAP", "PAS", "PAO",
        "PMD", "PMI", "PMN", "PMP", "PMS",
    ],
    "1+": [
        "IAI",
        "IMI",
    ],
    "2-": [
        "FAI", "FAN", "FAP",
        "FMI",
    ],
    "3-": [
        "AAD", "AAN", "AAP", "AAS", "AAO",
        "AMD", "AMN", "AMP", "AMS", "AMO",
    ],
    "3+": [
        "AAI",
        "AMI",
    ],
    "4-": [
        "XAI", "XAN", "XAP", "XAS",
    ],
    "4+": [
        "YAI",
    ],
    "5-": [
        "XMD", "XMI", "XMN", "XMP",
    ],
    "5+": [
        "YMI",
    ],
    "6-": [
        "APD", "APN", "APP", "APS", "APO",
    ],
    "6+": [
        "API",
    ],
    "7-": [
        "FPI", "FPP",
    ]
}

REVERSE_PARTS = {}

for part, tvm_list in PARTS.items():
    for tvm in tvm_list:
        REVERSE_PARTS[tvm] = part


def pp(key):
    return REVERSE_PARTS[key[0:3]]


STEM_GUESSES = defaultdict(lambda: defaultdict(set))

for book_num in [4, 23, 24, 25]:
    for row in morphgnt_rows(book_num):
        b, c, v = bcv_tuple(row["bcv"])
        if row["ccat-pos"] == "V-":
            lemma = row["lemma"]
            key = convert_parse(row["ccat-parse"])
            form = row["norm"]

            tags = set()

            c = form.count("/") + 1
            stem = ginflexion.find_stems(lemma, key, tags)
            generated = ginflexion.generate(lemma, key, tags)

            if stem:
                stem_guess = None
            else:
                stem_guess = [
                    stem for key, stem in
                    ginflexion.possible_stems(form, "^" + key + "$")]

            if [strip_length(w) for w in sorted(generated)] == \
                    [strip_length(w) for w in sorted(form.split("/"))]:
                correct = "✓"
            else:
                correct = "✕"
            if correct == "✕":
                if stem_guess:
                    STEM_GUESSES[lemma][pp(key)].add(frozenset(stem_guess))


for lemma, parts in sorted(STEM_GUESSES.items()):
    print()
    print("{}:".format(lemma))
    print("    stems:".format(lemma))
    for part, stem_sets in sorted(parts.items()):
        stem = set.intersection(*(set(s) for s in stem_sets))
        if len(stem) == 0:
            print("        {}: {}  # @0".format(part, stem_sets))
        elif len(stem) == 1:
            print("        {}: {}".format(part, stem.pop()))
        else:
            print("        {}: {}  # @m".format(part, stem))
