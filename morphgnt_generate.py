#!/usr/bin/env python3

import argparse

from pysblgnt import morphgnt_rows

from accent import strip_length  # , rebreath
from greek_inflexion import GreekInflexion
from morphgnt_utils import bcv_tuple, convert_parse
from test_generate import output_item


argparser = argparse.ArgumentParser(
    description="validate generation of correct forms")

argparser.add_argument(
    "books", metavar="BOOK_NUMBER", type=int, nargs="+",
    help="a book (Matt = 1)")

argparser.add_argument(
    "--lexicon", dest="lexicon",
    default="morphgnt_lexicon.yaml",
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
]

for book_num in args.books:
    for row in morphgnt_rows(book_num):
        b, c, v = bcv_tuple(row["bcv"])
        if row["ccat-pos"] == "V-":
            total_count += 1

            lemma = row["lemma"]
            key = convert_parse(row["ccat-parse"])
            form = row["norm"]

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

            if stem:
                stem_guess = None
            else:
                stem_guess = [
                    stem for key, stem in
                    ginflexion.possible_stems(form, "^" + key + "$")]

            if strip_length(form) in [
                    strip_length(w) for w in sorted(generated)]:
                correct = "✓"
            else:
                correct = "✕"
                incorrect_count += 1

            if debug or correct == "✕":
                output_item(
                    lemma, key, form,
                    stem, stem_guess, generated, correct)

print("{}/{} incorrect".format(incorrect_count, total_count))
