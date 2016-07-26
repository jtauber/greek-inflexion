#!/usr/bin/env python3

from generate import test_generate

test_generate("stemming.yaml", "pratt_lexicon.yaml", "pratt_test.yaml")
test_generate("stemming.yaml", "dik_lexicon.yaml", "dik_test.yaml")
test_generate("stemming.yaml", "ltrg_lexicon.yaml", "ltrg_test.yaml")
