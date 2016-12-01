#!/usr/bin/env python3

import argparse
from collections import defaultdict

from pysblgnt import morphgnt_rows

from accent import strip_length
from greek_inflexion import GreekInflexion
from morphgnt_utils import bcv_tuple, convert_parse, key_to_part


argparser = argparse.ArgumentParser(
    description="generate starting point for new lexicon")

argparser.add_argument(
    "books", metavar="BOOK_NUMBER", type=int, nargs="+",
    help="a book (Matt = 1)")

argparser.add_argument(
    "--lexicon", dest="lexicon",
    default="morphgnt_lexicon.yaml",
    help="path to initial stem lexicon file "
         "(defaults to morphgnt_lexicon.yaml)")

argparser.add_argument(
    "--stemming", dest="stemming",
    default="stemming.yaml",
    help="path to stemming rules file "
         "(defaults to stemming.yaml)")

args = argparser.parse_args()


ginflexion = GreekInflexion(
    args.stemming,
    args.lexicon,
    strip_length=True
)


STEM_GUESSES = defaultdict(lambda: defaultdict(set))

for book_num in args.books:
    for row in morphgnt_rows(book_num):
        b, c, v = bcv_tuple(row["bcv"])
        if row["ccat-pos"] == "V-":
            lemma = row["lemma"]
            key = convert_parse(row["ccat-parse"])
            form = row["norm"]

            tags = set([
                "final-nu-aai.3s",
                "oida-yai3p-variant",
                "no-final-nu-yai.3s",
                "late-pluperfect-singulars",
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

            if [strip_length(w) for w in sorted(generated)] == \
                    [strip_length(w) for w in sorted(form.split("/"))]:
                correct = "✓"
            else:
                correct = "✕"
            if correct == "✕":
                if stem_guess:
                    STEM_GUESSES[lemma][key_to_part(key)].add(
                        frozenset(stem_guess))


for lemma, parts in sorted(STEM_GUESSES.items()):
    print()
    print("{}:".format(lemma))
    print("    stems:".format(lemma))
    for part, stem_sets in sorted(parts.items()):
        stem = set.intersection(*(set(s) for s in stem_sets))
        if len(stem) == 0:
            print("        {}: {}  # @0".format(part, stem_sets))
        elif len(stem) == 1:
            print("        {}: {}  # @1".format(part, stem.pop()))
        else:
            print("        {}: {}  # @m".format(part, stem))
