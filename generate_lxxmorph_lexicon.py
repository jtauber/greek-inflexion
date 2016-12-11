#!/usr/bin/env python3

from collections import defaultdict
from unicodedata import normalize

from greekutils.beta2unicode import convert

from accent import strip_length
from greek_inflexion import GreekInflexion
from morphgnt_utils import key_to_part
from normalise import convert as norm_convert


book_to_num = {
    "1Mac": 24,
    "Jonah": 42,
    "Nah": 44,
}


def convert_parse(parse):
    if parse[2] in "DISOP":
        result = parse[:3] + "." + parse[3:]
    elif parse[2] in "N":
        result = parse
    if result[1] == "P" and result[0] not in "AF":
        result = result[0] + "M" + result[2:]
    return result


def get_words(filename):

    state = 0

    with open(filename) as f:
        for line in f:
            s = line.strip()
            if state == 0:  # expecting verse ref
                b, cv = s.split()
                c, v = cv.split(":")
                w = 0
                state = 1
            elif state == 1:    # expecting word line or blank link
                if s:
                    w += 1
                    if s[25] == "V":  # verb
                        yield {
                            "ref": "{:02d}.{:03d}.{:03d}.{:03d}".format(
                                book_to_num[b], int(c), int(v), w),
                            "word": normalize(
                                "NFKC", convert(s[:25].strip() + " ").strip()),
                            "type": s[25:28].strip(),
                            "parse": s[29:35].strip(),
                            "lemma": normalize(
                                "NFKC", convert(
                                    s[36:52].strip() + " ").strip()),
                            "preverb": normalize(
                                "NFKC", convert(s[53:].strip() + " ").strip()),
                        }
                else:
                    state = 0  # blank link so back to expecting verse ref


def trim_multiples(stem_set, part, lemma, parts):
    trimmed_stems = set()
    for stem in stem_set:
        if stem.endswith("0"):  # rarely a real stem
            pass
        elif part[0] == "3" and lemma.endswith("έω") and \
                stem.endswith("α{root}"):
            pass
        elif part[0] == "3" and lemma.endswith("όω") and \
                stem.endswith("{root}"):
            pass
        elif part[0] == "3" and lemma.endswith("όω") and \
                stem.endswith("{athematic}"):
            pass
        elif part[0] == "3" and lemma.endswith("άω") and \
                stem.endswith("α{root}"):
            pass
        elif part[0] == "1" and lemma.endswith("ω") and \
                stem.endswith("{athematic}"):
            pass
        elif part[0] == "1" and lemma.endswith("ομαι") and \
                stem.endswith("{athematic}"):
            pass
        elif part[0] == "4" and lemma.endswith("ω") and \
                stem.endswith("{athematic}"):
            pass
        elif part[0] == "4" and lemma.endswith("ομαι") and \
                stem.endswith("{athematic}"):
            pass
        elif part[0] == "1" and lemma.endswith("έω") and stem.endswith("ο"):
            pass
        elif part[0] == "1" and lemma.endswith("έω") and stem.endswith("α"):
            pass
        elif part[0] == "1" and lemma.endswith("έω") and stem.endswith("η"):
            pass
        elif part[0] == "1" and lemma.endswith("όω") and stem.endswith("ε"):
            pass
        elif part[0] == "1" and lemma.endswith("όω") and stem.endswith("α"):
            pass
        elif part[0] == "1" and lemma.endswith("όω") and stem.endswith("η"):
            pass
        elif part[0] == "1" and lemma.endswith("όω") and \
                stem.endswith("{athematic}"):
            pass
        elif part[0] == "1" and lemma.endswith("άω") and stem.endswith("η"):
            pass
        elif part[0] == "1" and lemma.endswith("άω") and stem.endswith("ε"):
            pass
        elif part[0] == "1" and lemma.endswith("άω") and stem.endswith("ο"):
            pass
        elif part[0] == "1" and lemma.endswith("έομαι") and stem.endswith("ο"):
            pass
        elif part[0] == "1" and lemma.endswith("όομαι") and stem.endswith("ε"):
            pass
        else:
            trimmed_stems.add(stem)

    if part == "3-" and len(stem_set) == 2:
        t = sorted(stem_set)
        if t[0] + "{2nd}" == t[1]:
            return "{}  # @1 2nd?".format(t[0])
        if t[1].endswith("ι{2nd}") and t[1] == t[0][:-5] + "ι{2nd}":
            return "{}  # @1".format(t[0])

    if len(trimmed_stems) == 1:
        return "{}  # @1".format(trimmed_stems.pop())
    elif len(trimmed_stems) == 0:
        return "{}  # @mm".format(stem_set)
    else:
        return "{}  # @m".format(trimmed_stems)


ginflexion = GreekInflexion(
    "stemming.yaml", "lxx_lexicon.yaml", strip_length=True
)


STEM_GUESSES = defaultdict(lambda: defaultdict(set))

for row in get_words("lxxmorph/44.Nahum.mlxx"):
    form = row["word"]
    preverb = row["preverb"]
    lemma = row["lemma"]
    key = convert_parse(row["parse"])
    if preverb:
        lemma = "+".join(preverb.split()) + "++" + lemma

    form = norm_convert(form, lemma, key)

    tags = set([
        "final-nu-aai.3s",
        # "oida-yai3p-variant",
        "no-final-nu-yai.3s",
        # "late-pluperfect-singulars",
        # "sigma-loss-pmd.2s",
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
