#!/usr/bin/env python3

from collections import defaultdict

from accent import strip_length
from greek_inflexion import GreekInflexion
from test_generate import output_item
from normalise import convert as norm_convert
from morphgnt_utils import key_to_part
from lxxmorph_utils import get_words, convert_parse


MLXX_FILES = [
    "lxxmorph/01.Gen.1.mlxx",
    "lxxmorph/02.Gen.2.mlxx",
    "lxxmorph/03.Exod.mlxx",
    "lxxmorph/04.Lev.mlxx",
    "lxxmorph/05.Num.mlxx",
    "lxxmorph/06.Deut.mlxx",
    "lxxmorph/07.JoshB.mlxx",
    "lxxmorph/08.JoshA.mlxx",
    "lxxmorph/09.JudgesB.mlxx",
    "lxxmorph/10.JudgesA.mlxx",
    "lxxmorph/11.Ruth.mlxx",

    "lxxmorph/19.2Esdras.mlxx",
    "lxxmorph/24.1Macc.mlxx",
    "lxxmorph/42.Jonah.mlxx",
    "lxxmorph/44.Nahum.mlxx",
]


debug = False

incorrect_count = 0
total_count = 0

summary_by_lemma = defaultdict(set)

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
            "sigma-loss-imi.2s",
            "late-pluperfect-singulars",
            "alt-eimi-imp",
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
            summary_by_lemma[lemma].add(key)
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
print(len(summary_by_lemma))
