#!/usr/bin/env python3

from pysblgnt import morphgnt_rows

from accent import strip_length  # , rebreath
from greek_inflexion import GreekInflexion
from morphgnt_utils import bcv_tuple, convert_parse
from test_generate import output_item


ginflexion = GreekInflexion("stemming.yaml", "morphgnt_lexicon.yaml")

debug = False


incorrect_count = 0
total_count = 0

for book_num in [4, 23, 24, 25]:
    for row in morphgnt_rows(book_num):
        b, c, v = bcv_tuple(row["bcv"])
        if row["ccat-pos"] == "V-":
            total_count += 1

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
