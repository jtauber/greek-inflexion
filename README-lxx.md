# lxx branch

This branch is where work on supporting the LXX forms is taking place.

It adds the following files:


* `lxxmorph/` -- directory of patch files to correct CATSS lxxmorph
* `lxx_lexicon.yaml` -- WIP stem dataset for LXX
* `lxxmorph_generate.py` -- script that goes through all the verb forms in `lxxmorph/` and validates that the code + dataset generates the correct form
* `generate_lxxmorph_lexicon.py` -- similar to `lxxmorph_generate.py` but instead of just validating and showing unexplainable forms, builds the starting point for a lexicon file to explain the forms
* `lxxmorph_utils.py` -- common code used by the above scripts


## Using `lxxmorph_generate.py`

The particular books to be tested are configured in the `MLXX_FILES` variable in the script.


## How to Extend Coverage of Lexicon

1. set `LXX_FILENAME` in `generate_lxxmorph_lexicon.py` to the path of the lxxmorph file you want to work on
2. add an entry in `book_to_num` in `lxxmorph_utils.py` to map book code used by file to book number
3. run `./generate_lxxmorph_lexicon.py > tmp1`
4. `cat lxx_lexicon.yaml tmp1 > tmp2`
5. `./sort_lexicon.py tmp2 > lxx_lexicon.yaml`
6. remove `tmp1` and `tmp2`
7. review all lines in `lxx_lexicon.yaml` that have `# @` (you can review about 10 a minute once you get good at it)

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

Update `MLXX_FILES` in `lxxmorph_generate.py` and run to test your new lexicon.

Failures could just be mistakes you made in step 7, could be missing `stemming.yaml` rules, or (actually most likely at this point) could be mistakes in the .`mlxx` file that need to be corrected.
