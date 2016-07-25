"""
encapsulates details of file format used for stemming.yaml, providing a
function for loading the file and populating StemmingRuleSet
"""

import yaml

from inflexion.stemming import StemmingRuleSet


def load_stemming(stemming_file):
    ruleset = StemmingRuleSet()

    with open(stemming_file) as f:
        stemming_dict = yaml.load(f)

    for key, rules in stemming_dict.items():

        while isinstance(rules, dict) and "ref" in rules:
            if rules["ref"] in stemming_dict:
                rules = stemming_dict[rules["ref"]]
            else:
                raise Exception("ref to {} which doesn't exist".format(
                    rules["ref"]))

        for rule in rules:
            if ";" in rule:
                rule, annotation = rule.split(";")
                ruleset.add(key, rule, {annotation})
            else:
                ruleset.add(key, rule)

    return ruleset
