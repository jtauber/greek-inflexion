>>> from greek_inflexion import GreekInflexion
>>> import pprint

Instantiate ``GreekInflexion`` with the stemming rule file and a lexicon file
(in this case, the lexicon for the paradigms in Pratt's Essentials).

>>> inflexion = GreekInflexion('stemming.yaml', 'test_data/pratt_lexicon.yaml')

Now, you can generate forms

>>> pprint.pprint(inflexion.generate('λύω', 'AAI.1S'))
defaultdict(<class 'list'>,
            {'ἔλυσα': [{'original_form': 'ελυσα',
                        'stem': 'ελυσ',
                        'stemming': {'base': 'ελυσ',
                                     'ending': 'α',
                                     'rule': SandhiRule('|><|α'),
                                     'used_default': True}}]})

or just find the stems:

>>> inflexion.find_stems('λύω', 'AAI.1S')
{'ελυσ'}


If the lexicon file has the necessary stem information, you can parse a form:

>>> inflexion.parse('ἔλυσα')
{('λύω', 'AAI.1S')}

This won't work if the information is not in the lexicon yet:

>>> inflexion.parse('ποιοῦμαι')
set()

You can, however, ask the system to conjecture what the possible stems might
be:

>>> pprint.pprint(sorted(inflexion.possible_stems('ποιοῦμαι')))
[('AAN', 'ποιουμ'),
 ('AAO.3S', 'ποιουμ'),
 ('AMD.2S', 'ποιουμ'),
 ('FMI.1S', 'ποι{contract}'),
 ('PMI.1S', 'ποιε'),
 ('PMI.1S', 'ποιο'),
 ('XMI.1S', 'ποιου')]

Notice that the system doesn't yet have any heuristics around likely stem
shape.

You can pass an optional regex to ``possible_stems`` if you have an idea of the
parsing:

>>> pprint.pprint(sorted(inflexion.possible_stems('ποιοῦμαι', '.+1S$')))
[('FMI.1S', 'ποι{contract}'),
 ('PMI.1S', 'ποιε'),
 ('PMI.1S', 'ποιο'),
 ('XMI.1S', 'ποιου')]
