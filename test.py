#!/usr/bin/env python3

from generate import test_generate

test_generate(
    "stemming.yaml",
    "test_data/pratt_lexicon.yaml",
    "test_data/pratt_test.yaml"
)

test_generate(
    "stemming.yaml",
    "test_data/dik_lexicon.yaml",
    "test_data/dik_test.yaml"
)

test_generate(
    "stemming.yaml",
    "test_data/ltrg_lexicon.yaml",
    "test_data/ltrg_test.yaml"
)
