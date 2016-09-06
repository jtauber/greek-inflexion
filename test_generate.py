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
                    print()
                    print(lemma, key, form)
                    if stem:
                        print("stem: {}".format(stem))
                    if stem_guess:
                        print("stem_guess: {}".format(stem_guess))
                    print("generate[{}/{}{}]{}".format(
                        len(generated), c, correct, ":" if generated else ""))
                    for generated_form, details in generated.items():
                        print("    - {}".format(generated_form))
                        for detail in details:
                            print("        {}".format(detail))
