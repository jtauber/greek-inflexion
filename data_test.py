#!/usr/bin/env python3

from test_generate import test_generate

test_generate(
    "stemming.yaml",
    "STEM_DATA/pratt_lexicon.yaml",
    "test_data/pratt_test.yaml"
)

test_generate(
    "stemming.yaml",
    "STEM_DATA/dik_lexicon.yaml",
    "test_data/dik_test.yaml"
)

# test_generate(
#     "stemming.yaml",
#     "STEM_DATA/ltrg_lexicon.yaml",
#     "test_data/ltrg_test.yaml"
# )
