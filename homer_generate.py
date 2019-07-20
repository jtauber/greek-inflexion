#!/usr/bin/env python3

from collections import defaultdict

from accent import strip_length
from greek_inflexion import GreekInflexion
from test_generate import output_item
from homer_utils import key_to_part


debug = False

incorrect_count = 0
total_count = 0

summary_by_lemma = defaultdict(set)

ginflexion = GreekInflexion(
    "stemming.yaml", "STEM_DATA/homer_lexicon.yaml"
)

first = True

FILENAME = "homer-data/verbs.tsv"
PART = []  # ["3-"]

with open(FILENAME) as f:
    for row in f:
        total_count += 1

        lemma, key, form = row.strip().split()
        if PART:
            if key_to_part(key) not in PART:
                continue

        tags = set([
            "fixed-final-nu-aai.3s",
            "no-final-nu-aai.3s",
            "no-final-nu-aao.3s",
            "no-final-nu-fai.3p",
            "no-final-nu-pai.3p",
            "no-final-nu-iai.3s",
            "no-final-nu-xai.3s",
            "no-final-nu-xai.3p",
            "no-final-nu-yai.3s",
            "no-final-nu-aps.3p",
            "no-final-nu-pai.3s",
            "no-final-nu-aas.3p",
            "no-final-nu-xas.3p",
            "no-sigma-loss-imi.2s",
            "alt-apo-pl",
            "Homer",
        ])

        c = form.count("/") + 1
        stem = ginflexion.find_stems(lemma, key, tags)
        generated = ginflexion.generate(lemma, key, tags)
        if strip_length(form) in [
                strip_length(w) for w in sorted(generated)]:
            correct = "✓"
        else:
            correct = "✕"
            incorrect_count += 1
            summary_by_lemma[lemma].add(key)
            if first:
                possible_stems = [
                    (key_to_part(a), b, a)
                    for a, b in ginflexion.possible_stems(form)
                ]
                likely_stems = [
                    (key_to_part(a), b)
                    for a, b in ginflexion.possible_stems(
                        form, "^" + key + "$")
                ]
                possible_parses = []
                for plemma, pparse in ginflexion.parse(form):
                    possible_parses.append((
                        plemma,
                        pparse,
                        set(ginflexion.generate(plemma, pparse, tags))
                    ))

        if debug or correct == "✕":
            if first:
                output_item(
                    lemma, key, key_to_part(key), form, None,
                    stem, possible_stems, likely_stems, possible_parses,
                    generated, correct)
            # if len(likely_stems) == 1:
            #     print(lemma, likely_stems[0][0], likely_stems[0][1])
            first = False

print()
print("{}/{} incorrect".format(incorrect_count, total_count))
print(len(summary_by_lemma))
