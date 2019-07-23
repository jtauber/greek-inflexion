#!/usr/bin/env python3

from collections import defaultdict

from accent import strip_length
from greek_inflexion import GreekInflexion
from morphgnt_utils import key_to_part
from normalise import convert as norm_convert
from lxxmorph_utils import get_words, convert_parse, trim_multiples


ginflexion = GreekInflexion(
    "stemming.yaml", "STEM_DATA/lxx_lexicon.yaml", strip_length=True
)

LXX_FILENAME = "lxxmorph/12.1Sam.mlxx"

STEM_GUESSES = defaultdict(lambda: defaultdict(set))

for row in get_words(LXX_FILENAME):
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
        "fpi.2s-ει",
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
            ginflexion.possible_stems2(form, "^" + key + "$")]

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
    for part, stem_sets in sorted(
            parts.items(), key=lambda x: (x[0][0], {"-": 0, "+": 1}[x[0][1]])):
        stem = set.intersection(*(set(s) for s in stem_sets))
        if len(stem) == 0:
            print("        {}: {}  # @0".format(part, stem_sets))
        elif len(stem) == 1:
            print("        {}: {}  # @1".format(part, stem.pop()))
        else:
            print("        {}: {}".format(part, trim_multiples(
                stem, part, lemma, parts)))
