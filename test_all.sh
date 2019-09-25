#!/bin/sh

echo "\nunit tests"
python unit_tests.py > /dev/null
echo "\nclassical paradigm tests"
python data_test.py
echo "\nregression tests"
python regression_tests.py
echo "\ndoctests"
python -m doctest examples.rst
echo "\nmorphgnt tests"
python morphgnt_generate.py 1 2 3 4 5 6 7 9 10 11 12 13 14 15 16 17 18 19 20 23 24 25 26 27
echo "\nhomer paradigm tests"
python homer_generate_paradigms.py
