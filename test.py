#!/usr/bin/env python3

import unittest

from greek_inflexion import GreekInflexion


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
            {'ελυσ'}
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
                ('XMI.1S', 'ποιου')
            ]
        )

    def test_possible_stems2(self):
        self.assertEqual(
            sorted(self.inflexion.possible_stems('ποιοῦμαι', '.+1S$')),
            [
                ('FMI.1S', 'ποι{contract}'),
                ('PMI.1S', 'ποιε'),
                ('PMI.1S', 'ποιο'),
                ('XMI.1S', 'ποιου')
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
