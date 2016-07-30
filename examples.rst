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

or parse them

>>> inflexion.parse("ελυσα")
{('λύω', 'AAI.1S')}

or find the possible stems

>>> inflexion.find_stems('λύω', 'AAI.1S')
{'ελυσ'}
