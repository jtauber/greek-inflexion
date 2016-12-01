# morphgnt branch

This branch is where work on supporting the MorphGNT forms is taking place.

It adds the following files:


* `morphgnt_johannine_lexicon.yaml` -- the stem dataset for the verbs in gospel/epistles of John
* `morphgnt_generate.py` -- script that goes through (using `py-sblgnt`) all the verb forms in the gospel/epistles of John (or any other books, just change line 40) and validate that the code + dataset generates the correct form
* `generate_morphgnt_lexicon.py` -- similar to `morphgnt_generate.py` but instead of just validating an showing unexplainable forms, builds the starting point for a lexicon file to explain the forms
* `make_morphgnt_test.py` -- script for generating a YAML test file (like those in `test_data/`) based on verbs in John (or change line 10)
* `make_morphgnt_nominal_test.py` -- like `make-morphgnt_test.py` but for nouns and adjectives.
* `morphgnt_utils.py` -- common code used by the above scripts
