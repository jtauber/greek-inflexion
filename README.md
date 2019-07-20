# greek-inflexion

[![Build Status](https://travis-ci.org/jtauber/greek-inflexion.svg)](https://travis-ci.org/jtauber/greek-inflexion)

A Python 3 library for generating (and analyzing) Ancient Greek inflectional
paradigms.

`greek-inflexion` builds on my generic `inflexion` library, adding a stem
database and ending rules for Ancient Greek along with accentuation logic
built on top of my `greek-accentuation` library.

It can precisely generate (i.e. without over-generation) all the forms in the
verbal paradigms in Louise Pratt's _The Essentials of Greek Grammar_, Helma
Dik's Nifty Greek Handouts, and Keller and Russell's _Learn to Read Greek_. It
can also generate the nouns in Pratt.

For each generated form, it can show the stem, ending, and morphophonological
(sandhi) rule applied.

Entire paradigms can be generated at once in the same YAML format used for
tests.

The library can also parse forms whose information is in the given lexicon or
conjecture possible stem information if not.

For more of my work on linguistics and Ancient Greek, see
<http://jktauber.com/>.


## Documentation

To run the full data tests from Pratt, Dik, and Keller and Russell, just run
`./data_test.py`.

For the noun data tests, run `./noun_data_test.py`.

See `examples.rst` for individual usage examples of the library.


## TODO

Most of these are partially done elsewhere and I'm in the process of cleaning
them up and moving them into this repo.

 - reduction of repetition in ending rules
 - better tools for analysis of forms
 - better stem shape heuristics when conjecturing stems
 - better stem conjecture when multiple forms available
 - richer stem database from principal parts lists
 - support for more nominal forms
