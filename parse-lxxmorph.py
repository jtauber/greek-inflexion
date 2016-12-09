#!/usr/bin/env python3

from unicodedata import normalize

from greekutils.beta2unicode import convert
from accent import strip_length
from greek_inflexion import GreekInflexion

from test_generate import output_item

book_to_num = {
    "1Mac": 24,
}


def convert_parse(parse):
    if parse[2] in "DISOP":
        return parse[:3] + "." + parse[3:]
    elif parse[2] in "N":
        return parse


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


debug = False

incorrect_count = 0
total_count = 0

ginflexion = GreekInflexion("stemming.yaml", "morphgnt_lexicon.yaml")

for row in get_words("lxxmorph/24.1Macc.mlxx"):
    total_count += 1

    form = row["word"]
    lemma = row["lemma"]
    key = convert_parse(row["parse"])

    tags = set()

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
        stem_guess = [
            possible_stem for key, possible_stem in
            ginflexion.possible_stems(form, "^" + key + "$")]

    if debug or correct == "✕":
        output_item(
            lemma, key, form,
            stem, stem_guess, generated, correct)

print("{}/{} incorrect".format(incorrect_count, total_count))
