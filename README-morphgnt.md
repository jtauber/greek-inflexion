# morphgnt branch

This branch is where work on supporting the MorphGNT forms is taking place.

It adds the following files:

* `morphgnt_generate.py` -- go through (using `py-sblgnt`) all the verb forms in the gospel/epistles of John (or any other books, just change line 40) and validate that the code + dataset generates the correct form.
 `morphgnt_johannine_lexicon.yaml` -- the stem dataset for the verbs in gospel/epistles of John.
* `generate_morphgnt_lexicon.py`
* `make_morphgnt_test.py`
* `make_morphgnt_nominal_test.py`
