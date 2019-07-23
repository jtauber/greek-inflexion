#!/usr/bin/env python3

import argparse

from pysblgnt import morphgnt_rows

from accent import strip_length  # , rebreath
from greek_inflexion import GreekInflexion
from morphgnt_utils import bcv_tuple, convert_parse, key_to_part
from test_generate import output_item


argparser = argparse.ArgumentParser(
    description="validate generation of correct forms")

argparser.add_argument(
    "books", metavar="BOOK_NUMBER", type=int, nargs="+",
    help="a book (Matt = 1)")

argparser.add_argument(
    "--lexicon", dest="lexicon",
    default="STEM_DATA/morphgnt_lexicon.yaml",
    help="path to stem lexicon file "
         "(defaults to morphgnt_lexicon.yaml)")

argparser.add_argument(
    "--stemming", dest="stemming",
    default="stemming.yaml",
    help="path to stemming rules file "
         "(defaults to stemming.yaml)")

args = argparser.parse_args()

ginflexion = GreekInflexion(args.stemming, args.lexicon)

debug = False


incorrect_count = 0
total_count = 0

IGNORE_LIST = [
    "κουμ",
    "εφφαθα",
    "σαβαχθάνι",
    "θά",
]

for book_num in args.books:
    for row in morphgnt_rows(book_num):
        b, c, v = bcv_tuple(row["bcv"])
        if row["ccat-pos"] == "V-":
            total_count += 1

            lemma = row["lemma"]
            key = convert_parse(row["ccat-parse"])
            form = row["norm"]

            # need to just do this in MorphGNT itself
            if key in ["AAO.3P", "PAO.3P"]:
                form = form.replace("(ν)", "ν")

            if lemma in IGNORE_LIST:
                continue

            tags = set([
                "final-nu-aai.3s",
                "oida-yai3p-variant",
                "no-final-nu-yai.3s",
                "late-pluperfect-singulars",
                "sigma-loss-pmd.2s",
                "HGrk",
            ])

            c = form.count("/") + 1
            stem = ginflexion.find_stems(lemma, key, tags)
            generated = ginflexion.generate(lemma, key, tags)

            if strip_length(form) in [
                    strip_length(w) for w in sorted(generated)]:
                correct = "✓"
                stem_guess = None
            else:
                correct = "✕"
                incorrect_count += 1
                possible_stems = [
                    (key_to_part(a), b, a)
                    for a, b in ginflexion.possible_stems(form)
                ]
                likely_stems = [
                    (key_to_part(a), b)
                    for a, b in ginflexion.possible_stems(
                        form, "^" + key + "$")
                ]
                possible_parses = ginflexion.parse(form)

            if debug or correct == "✕":
                output_item(
                    lemma, key, key_to_part(key), form, None,
                    stem, possible_stems, likely_stems, possible_parses,
                    generated, correct)

print("{}/{} incorrect".format(incorrect_count, total_count))
