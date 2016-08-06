#!/usr/bin/env python3

from test_generate import test_generate

test_generate(
    "noun_stemming.yaml",
    "test_data/pratt_noun_lexicon.yaml",
    "test_data/pratt_noun_test.yaml"
)
