#!/usr/bin/env python3

import unittest

from fileformat import load_stemming, load_lexicon
from fileformat import RefDoesNotExistException
from greek_inflexion import GreekInflexion


class FileFormatTest(unittest.TestCase):

    def test_bad_ref(self):
        with self.assertRaises(RefDoesNotExistException):
            load_stemming("test_files/bad_ref.yaml")

    def test_stemming(self):
        s = load_stemming("test_files/stemming_test.yaml")
        self.assertEqual(s.key_to_rules["bar"][0].surface, "ace")
        self.assertEqual(s.key_to_rules["foo"][1].tags, {"baz"})

    def test_lexicon(self):
        lexicon, form_override, accent_override = load_lexicon(
            "test_files/lexicon_test.yaml")
        self.assertEqual(form_override[("lemma2", "PAI.3S")], "blah")
        self.assertEqual(accent_override["lemma2"], [('PAI', 'blah')])
        self.assertEqual(
            lexicon.lemma_to_stems["lemma2"], [
                ('I', 'baz', {'+z'}),
                ('P', 'bar', set()),
                ('foo', 'bar', set())
            ])


class InflexionTest(unittest.TestCase):

    def setUp(self):
        self.inflexion = GreekInflexion(
            "stemming.yaml",
            "test_data/pratt_lexicon.yaml"
        )

    def test_generate(self):
        self.inflexion.generate('λύω', 'AAI.1S')
        # @@@

    def test_find_stems(self):
        self.assertEqual(
            self.inflexion.find_stems('λύω', 'AAI.1S'),
            {'ἐλυσ'}
        )

    def test_parse1(self):
        self.assertEqual(
            self.inflexion.parse('ἔλυσα'),
            {('λύω', 'AAI.1S')}
        )

    def test_parse2(self):
        self.assertEqual(
            self.inflexion.parse('ποιοῦμαι'),
            set()
        )

    def test_possible_stems1(self):
        self.assertEqual(
            sorted(self.inflexion.possible_stems('ποιοῦμαι')),
            [
                ('AAN', 'ποιουμ'),
                ('AAO.3S', 'ποιουμ'),
                ('AMD.2S', 'ποιουμ'),
                ('FMI.1S', 'ποι{contract}'),
                ('PMI.1S', 'ποιε'),
                ('PMI.1S', 'ποιο'),
                ('XMI.1S', 'ποιου'),
                ('ZMI.1S', 'ποι{contract}'),
            ]
        )

    def test_possible_stems2(self):
        self.assertEqual(
            sorted(self.inflexion.possible_stems('ποιοῦμαι', '.+1S$')),
            [
                ('FMI.1S', 'ποι{contract}'),
                ('PMI.1S', 'ποιε'),
                ('PMI.1S', 'ποιο'),
                ('XMI.1S', 'ποιου'),
                ('ZMI.1S', 'ποι{contract}'),
            ]
        )

    def test_conjugate(self):
        self.inflexion.conjugate(
            "λύω", "PAI", "AAI", tags={"final-nu-aai.3s"}
        )
        # @@@

    def test_decline(self):
        self.inflexion.decline(
            "λύω", "PAP"
        )
        # @@@


if __name__ == "__main__":
    unittest.main()
