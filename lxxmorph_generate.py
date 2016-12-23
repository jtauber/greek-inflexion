#!/usr/bin/env python3

from unicodedata import normalize

from greekutils.beta2unicode import convert

from accent import strip_length
from greek_inflexion import GreekInflexion
from test_generate import output_item
from normalise import convert as norm_convert
from morphgnt_utils import key_to_part
from lxxmorph_utils import get_words, convert_parse


MLXX_FILES = [
    "lxxmorph/24.1Macc.mlxx",
    "lxxmorph/42.Jonah.mlxx",
    "lxxmorph/44.Nahum.mlxx",
    "lxxmorph/19.2Esdras.mlxx",
    "lxxmorph/01.Gen.1.mlxx",
    "lxxmorph/02.Gen.2.mlxx",
    "lxxmorph/03.Exod.mlxx",
]


debug = False

incorrect_count = 0
total_count = 0

ginflexion = GreekInflexion("stemming.yaml", "lxx_lexicon.yaml")

for filename in MLXX_FILES:
    for row in get_words(filename):
        total_count += 1

        line = row["line"]
        form = row["word"]
        preverb = row["preverb"]
        lemma = row["lemma"]
        key = convert_parse(row["parse"])
        if preverb:
            lemma = "+".join(preverb.split()) + "++" + lemma

        form = norm_convert(form, lemma, key)

        tags = set([
            "final-nu-aai.3s",
            "alt-apo-pl",
            "sigma-loss-pmd.2s",
            "HGrk",
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
            possible_stems = [
                (key_to_part(a), b, a)
                for a, b in ginflexion.possible_stems(form)
            ]
            likely_stems = [
                (key_to_part(a), b)
                for a, b in ginflexion.possible_stems(form, "^" + key + "$")
            ]
            possible_parses = ginflexion.parse(form)

        if debug or correct == "✕":
            output_item(
                lemma, key, key_to_part(key), form, line,
                stem, possible_stems, likely_stems, possible_parses,
                generated, correct)

print()
print("{}/{} incorrect".format(incorrect_count, total_count))
