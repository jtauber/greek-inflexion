from collections import defaultdict

import yaml

from inflexion import Inflexion

from accent import calculate_accent, strip_length, debreath

from fileformat import load_stemming, load_lexicon


def generate_greek(inflexion, lemma, key, tags, accent_override):
    generated = defaultdict(list)
    for orig_form, details in inflexion.generate(
            lemma, key, tags).items():
        for detail in details:
            accent_form = calculate_accent(
                orig_form, key, lemma, detail["stem"],
                inflexion, accent_override)
            detail.update({"original_form": orig_form})
            generated[accent_form].append(detail)
    return generated


def test_generate(
    stemming_file, lexicon_file, test_file,
    global_tags=None, debug=False
):
    """
    generates all the forms in the test_file using the lexicon_file and
    stemming_file and outputs any discrepancies.
    """

    ## load the stemming rule set

    ruleset = load_stemming(stemming_file)

    ## load the stem lexicon

    lexicon, form_override, accent_override = load_lexicon(
        lexicon_file, pre_processor=debreath)

    ## set up Inflexion

    inflexion = Inflexion()
    inflexion.add_lexicon(lexicon)
    inflexion.add_stemming_rule_set(ruleset)

    ## work through test file

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
                stem = lexicon.find_stems(lemma, key, tags)
                if (lemma, key) in form_override:
                    pass
                else:

                    generated = generate_greek(
                        inflexion, lemma, key, tags, accent_override)

                    if [strip_length(w) for w in sorted(generated)] == \
                            [strip_length(w) for w in sorted(form.split("/"))]:
                        correct = "✓"
                    else:
                        correct = "✕"
                    if debug or correct == "✕":
                        print()
                        print(lemma, key, form)
                        print("stem: {}".format(stem))
                        print("generate[{}/{}{}]:".format(
                            len(generated), c, correct))
                        for generated_form, details in generated.items():
                            print("    - {}".format(generated_form))
                            for detail in details:
                                print("        {}".format(detail))
