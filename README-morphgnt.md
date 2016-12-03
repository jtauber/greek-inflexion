# morphgnt branch

This branch is where work on supporting the MorphGNT forms is taking place.

It adds the following files:


* `morphgnt_johannine_lexicon.yaml` -- the stem dataset for the verbs in gospel/epistles of John
* `morphgnt_lexicon.yaml` -- WIP stem dataset with more verbs
* `morphgnt_generate.py` -- script that goes through (using `py-sblgnt`) all the verb forms in given NT books and validates that the code + dataset generates the correct form
* `generate_morphgnt_lexicon.py` -- similar to `morphgnt_generate.py` but instead of just validating and showing unexplainable forms, builds the starting point for a lexicon file to explain the forms
* `make_morphgnt_test.py` -- script for generating a YAML test file (like those in `test_data/`) based on verbs in John (or change line 10)
* `make_morphgnt_nominal_test.py` -- like `make-morphgnt_test.py` but for nouns and adjectives.
* `morphgnt_utils.py` -- common code used by the above scripts


## Using `morphgnt_generate.py`

To test John's gospel:

```
$ ./morphgnt_generate.py 4
```

To test the Johannine Epistles:

```
$ ./morphgnt_generate.py 23 24 25
```

`morphgnt_generate.py` also takes `--lexicon` and `--stemming` arguments to change the stem lexicon and stemming rule files respectively.


## How to Extend Coverage of Lexicon

1. run `generate_morphgnt_lexicon.py` on the book(s) you want to add coverage for: `./generate_morphgnt_lexicon.py BOOK1 BOOK2 ... > tmp1`
2. `cat morphgnt_lexicon.yaml tmp1 > tmp2`
3. `./sort_lexicon.py tmp2 > morphgnt_lexicon.yaml`
4. review all lines in `morphgnt_lexicon.yaml` that have `# @` (you can review about 10 a minute once you get good at it)

`@m` means multiple possible stems, for example:

```
ἀγνοέω:
    stems:
        1-: {'ἀγνοου{athematic}', 'ἀγνοε', 'ἀγνοο'}  # @m
```

which should be manually corrected to:

```
ἀγνοέω:
    stems:
        1-: ἀγνοε
```

`@1` means a single possible stem. Verify and make sure if the lemma already exists that the new stem is moved in with the others.

For example:

```
ἀποκόπτω:
    stems:
        3+: ἀπεκοψ
    stems:
        2-: ἀποκοψ  # @1
```

needs to be changed to

```
ἀποκόπτω:
    stems:
        2-: ἀποκοψ
        3+: ἀπεκοψ
    stems:
```

`@0` means no stem could be guessed. This normally means a missing `stemming.yaml` rule.

Run `./morphgnt_generate.py` with appropriate arguments to test your new lexicon.

Failures could just be mistakes you made in step 5 or could be missing `stemming.yaml` rules.
