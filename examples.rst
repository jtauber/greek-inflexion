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
{'ἐλυσ'}


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


``GreekInflexion`` can also generate paradigms in a YAML format that can then
be used for testing.

>>> inflexion.conjugate("λύω", "PAI", "AAI", tags={"final-nu-aai.3s"})
-
    lemma: λύω
<BLANKLINE>
    tags:
      - final-nu-aai.3s
<BLANKLINE>
    PAI.1S: λῡ́ω
    PAI.2S: λῡ́εις
    PAI.3S: λῡ́ει
    PAI.1P: λῡ́ομεν
    PAI.2P: λῡ́ετε
    PAI.3P: λῡ́ουσι(ν)
<BLANKLINE>
    AAI.1S: ἔλυσα
    AAI.2S: ἔλυσας
    AAI.3S: ἔλυσε(ν)
    AAI.1P: ἐλύσαμεν
    AAI.2P: ἐλύσατε
    AAI.3P: ἔλυσαν
<BLANKLINE>
<BLANKLINE>


>>> inflexion.decline("λύω", "PAP")
-
    lemma: λύω
<BLANKLINE>
    PAP.NSM: λῡ́ων
    PAP.GSM: λῡ́οντος
    PAP.DSM: λῡ́οντι
    PAP.ASM: λῡ́οντα
    PAP.VSM: λῡ́ων
    PAP.NPM: λῡ́οντες
    PAP.VPM: λῡ́οντες
    PAP.GPM: λῡόντων
    PAP.DPM: λῡ́ουσι(ν)
    PAP.APM: λῡ́οντας
<BLANKLINE>
    PAP.NSF: λῡ́ουσα
    PAP.GSF: λῡούσης
    PAP.DSF: λῡούσῃ
    PAP.ASF: λῡ́ουσαν
    PAP.VSF: λῡ́ουσα
    PAP.NPF: λῡ́ουσαι
    PAP.VPF: λῡ́ουσαι
    PAP.GPF: λῡουσῶν
    PAP.DPF: λῡούσαις
    PAP.APF: λῡούσᾱς
<BLANKLINE>
    PAP.NSN: λῦον
    PAP.GSN: λῡ́οντος
    PAP.DSN: λῡ́οντι
    PAP.ASN: λῦον
    PAP.VSN: λῦον
    PAP.NPN: λῡ́οντα
    PAP.VPN: λῡ́οντα
    PAP.GPN: λῡόντων
    PAP.DPN: λῡ́ουσι(ν)
    PAP.APN: λῡ́οντα
<BLANKLINE>
<BLANKLINE>
