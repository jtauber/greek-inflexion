#!/usr/bin/env python3

from generate import generate

generate("stemming.yaml", "pratt_lexicon.yaml", "pratt_test.yaml")
generate("stemming.yaml", "dik_lexicon.yaml", "dik_test.yaml")
