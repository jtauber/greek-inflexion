import yaml

from accent import strip_length

from greek_inflexion import GreekInflexion


def output_detail(detail):
    print("          -")

    if "stem" in detail:
        print("            stem: {}".format(detail["stem"]))

    if "stemming" in detail:
        print("            stemming:")
        print("                base: {}".format(detail["stemming"]["base"]))
        print("                ending: {}".format(
            detail["stemming"]["ending"]))
        print("                rule: \"{0.a}|{0.b}>{0.c}<{0.d}|{0.e}\"".format(
            detail["stemming"]["rule"]))
        print("                used_default: {}".format(
            detail["stemming"]["used_default"]))

    if "original_form" in detail:
        print("            original_form: {}".format(detail["original_form"]))
    if "accent_notes" in detail:
        print("            accent_notes: {}".format(detail["accent_notes"]))

    if "override" in detail:
        print("            override: {}".format(detail["override"]))


def output_item(
        lemma, segmented_lemma, key, part, form, line, stem,
        possible_stems, likely_stems, possible_parses, generated, correct):
    print()
    print("-")
    print("    form: {}".format(form))
    print("    correct: \"{}/{} {}\"".format(
        len(generated), form.count("/") + 1, correct))
    print("    generated:")
    for generated_form in generated.keys():
        print(f"        - {generated_form}")
    print()
    print("    lemma: {}".format(lemma))
    if segmented_lemma:
        print("    segmented_lemma: {}".format(segmented_lemma))
    print("    key: {}".format(key))
    print("    part: {}".format(part))
    if line:
        print("    line: {}".format(line))
    print()

    if stem:
        if len(stem) == 1:
            print("    stem: {}".format(list(stem)[0]))
        else:
            print("    stem: {}".format(list(stem)))

    if likely_stems:
        print("    likely_stems:")
        for likely_stem in sorted(likely_stems):
            print("        {}: {}".format(*likely_stem))

    if possible_stems:
        print("    possible_stems:")
        for possible_stem in sorted(possible_stems):
            print("        - {} {}  # {}".format(*possible_stem))

    if possible_parses:
        print("    possible_parses:")
        for guess in sorted(possible_parses):
            print("        - {}".format(guess))

    if generated:
        print("    generated:")

    for generated_form, details in generated.items():
        print("      -")
        print("        form: {}".format(generated_form))
        print("        details:")
        for detail in details:
            output_detail(detail)


def test_generate(
    stemming_file, lexicon_file, test_file,
    global_tags=None, debug=False
):
    """
    generates all the forms in the test_file using the lexicon_file and
    stemming_file and outputs any discrepancies (or everything if debug on)
    """

    ginflexion = GreekInflexion(stemming_file, lexicon_file)

    with open(test_file) as f:
        for test in yaml.safe_load(f):
            source = test.pop("source", None)
            test.pop("test_length", False)
            lemma = test.pop("lemma")
            tags = set(test.pop("tags", []))
            if source:
                tags.update({source})
            if global_tags:
                tags.update(global_tags)

            segmented_lemma = ginflexion.segmented_lemmas.get(lemma)
            for key, form in sorted(test.items()):
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
                if debug or correct == "✕":
                    output_item(
                        lemma, segmented_lemma, key, None, form, None, stem,
                        stem_guess, None, None, generated, correct)
