from collections import defaultdict

import yaml

from inflexion.lexicon import Lexicon
from inflexion import Inflexion

from characters import strip_length

from accent import debreath, calculate_accent

from fileformat import load_stemming


def generate(
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

    lexicon = Lexicon()

    partnum_to_key_regex = {
        "1-": "P",
        "1-A": "PA",
        "1-M": "PM",
        "1+": "I",
        "2-": "F[AM]",
        "2-A": "FA",
        "2-M": "FM",
        "3-": "A[AM][NPDSO]",
        "3+": "A[AM]I",
        "3+A": "AAI",
        "3+M": "AMI",
        "4-": "XA",
        "4+": "YA",
        "5-": "X[MP]",
        "5+": "Y[MP]",
        "6-": "AP[NPDSO]",
        "6+": "API",
        "7-": "FP",
    }

    form_override = {}
    accent_override = defaultdict(list)

    with open(lexicon_file) as f:
        for lemma, entry in yaml.load(f).items():
            if "stems" not in entry:
                continue
            stems = []
            for partnum, stems in sorted(entry["stems"].items()):
                key_regex = partnum_to_key_regex[partnum]
                for stem in stems.split("/"):
                    if ";" in stem:
                        stem, tag = stem.split(";")
                        tag = {tag}
                    else:
                        tag = set()
                    lexicon.add(lemma, key_regex, debreath(stem), tag)
            for key_regex, stems in entry.get("stem_overrides", []):
                if stems is None:
                    continue
                for stem in stems.split("/"):
                    if ";" in stem:
                        stem, tag = stem.split(";")
                        tag = {tag}
                    else:
                        tag = set()
                    lexicon.add(lemma, key_regex, debreath(stem), tag)
            for key, form in entry.get("forms", {}).items():
                form_override[(lemma, key)] = form
            for key_regex, form in entry.get("accents", []):
                accent_override[lemma].append((key_regex, form))

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
                    generated = defaultdict(list)
                    for orig_form, details in inflexion.generate(
                            lemma, key, tags).items():
                        for detail in details:
                            accent_form = calculate_accent(
                                orig_form, key, lemma, detail["stem"],
                                inflexion, accent_override)
                            detail.update({"original_form": orig_form})
                            generated[accent_form].append(detail)
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
