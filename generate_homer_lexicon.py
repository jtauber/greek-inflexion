#!/usr/bin/env python3

from collections import defaultdict

from accent import strip_length
from greek_inflexion import GreekInflexion
from homer_utils import key_to_part, trim_multiples


ginflexion = GreekInflexion(
    "stemming.yaml", "STEM_DATA/homer_lexicon.yaml"
)

STEM_GUESSES = defaultdict(lambda: defaultdict(set))

with open("homer-data/verbs.tsv") as f:
    for row in f:
        lemma, key, form = row.strip().split("\t")

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
            if False:
                print("        {}: {}  # @0".format(part, stem_sets))
        elif len(stem) == 1:
            print("        {}: {}  # @1".format(part, stem.pop()))
        else:
            if False:
                print("        {}: {}".format(part, trim_multiples(
                    stem, part, lemma, parts)))
