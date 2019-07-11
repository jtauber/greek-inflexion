"""
encapsulates details of file format used for stemming.yaml, and lexicon YAMLs,
providing functions for loading the file and populating StemmingRuleSet or
Lexicon (with form and accent overrides)
"""

from collections import defaultdict

import yaml

from greek_accentuation.characters import strip_length as do_strip_length

from inflexion.lexicon import Lexicon
from inflexion.stemming import StemmingRuleSet


class RefDoesNotExistException(Exception):
    pass


def load_stemming(stemming_file, strip_length=False):
    ruleset = StemmingRuleSet()

    with open(stemming_file) as f:
        stemming_dict = yaml.safe_load(f)

    for key, rules in stemming_dict.items():

        while isinstance(rules, dict) and "ref" in rules:
            if rules["ref"] in stemming_dict:
                rules = stemming_dict[rules["ref"]]
            else:
                raise RefDoesNotExistException(
                    "ref to {} which doesn't exist".format(
                        rules["ref"]))

        for rule in rules:
            if strip_length:
                rule = do_strip_length(rule)
            if ";" in rule:
                rule, annotation = rule.split(";")
                ruleset.add(key, rule, {annotation})
            else:
                ruleset.add(key, rule)

    return ruleset


def split_stem_tags(stems):
    for stem in stems.split("/"):
        if ";" in stem:
            stem, tag = stem.split(";")
            tag = {tag}
        else:
            tag = set()

        yield stem, tag


def load_lexicon(lexicon_file, pre_processor=lambda x: x):
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
        "8-": "Z[MP]",
        "M": "..M",
        "F": "..F",
        "N": "..N",
    }

    form_override = {}
    accent_override = defaultdict(list)

    with open(lexicon_file) as f:

        for lemma, entry in yaml.safe_load(f).items():

            if entry:
                if "stems" in entry:

                    stems = []

                    for partnum, stems in sorted((
                        entry["stems"] if entry.get("stems") else {}
                    ).items()):

                        key_regex = partnum_to_key_regex[partnum]

                        for stem, tag in split_stem_tags(stems):
                            lexicon.add(
                                lemma, key_regex, pre_processor(stem), tag)

                    for key_regex, stems in entry.get("stem_overrides", []):

                        if stems is None:
                            continue

                        for stem, tag in split_stem_tags(stems):
                            lexicon.add(
                                lemma, key_regex, pre_processor(stem), tag)

                for key, form in entry.get("forms", {}).items():
                    form_override[(lemma, key)] = form

                for key_regex, form in entry.get("accents", []):
                    accent_override[lemma].append((key_regex, form))

    return lexicon, form_override, accent_override
