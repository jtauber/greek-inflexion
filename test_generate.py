import yaml

from accent import strip_length

from greek_inflexion import GreekInflexion


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
        for test in yaml.load(f):
            source = test.pop("source", None)
            test.pop("test_length", False)
            lemma = test.pop("lemma")
            tags = set(test.pop("tags", []))
            if source:
                tags.update({source})
            if global_tags:
                tags.update(global_tags)

            for key, form in sorted(test.items()):
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
                if debug or correct == "✕":
                    print("-")
                    print("    lemma: {}".format(lemma))
                    print("    key: {}".format(key))
                    print("    form: {}".format(form))
                    if stem:
                        if len(stem) == 1:
                            print("    stem: {}".format(list(stem)[0]))
                        else:
                            print("    stem: {}".format(list(stem)))
                    if stem_guess:
                        print("    stem_guess: {}".format(stem_guess))
                    print("    correct: \"[{}/{}{}]\"".format(
                        len(generated), c, correct))
                    print("    generated:")
                    for generated_form, details in generated.items():
                        print("      -")
                        print("        form: {}".format(generated_form))
                        print("        details:")
                        for detail in details:
                            print("          -")
                            if "stem" in detail:
                                print("            stem: {}".format(detail["stem"]))
                            if "stemming" in detail:
                                print("            stemming:")
                                print("                base: {}".format(detail["stemming"]["base"]))
                                print("                ending: {}".format(detail["stemming"]["ending"]))
                                print("                rule: \"{0.a}|{0.b}>{0.c}<{0.d}|{0.e}\"".format(detail["stemming"]["rule"]))
                                print("                used_default: {}".format(detail["stemming"]["used_default"]))
                            if "original_form" in detail:
                                print("            original_form: {}".format(detail["original_form"]))
                            if "override" in detail:
                                print("            override: {}".format(detail["override"]))
