>>> from greek_inflexion import GreekInflexion
>>> import pprint

Instantiate ``GreekInflexion`` with the stemming rule file and a lexicon file
(in this case, the lexicon for the paradigms in Pratt's Essentials).

>>> inflexion = GreekInflexion('stemming.yaml', 'STEM_DATA/pratt_lexicon.yaml')

Now, you can generate forms

>>> pprint.pprint(inflexion.generate('λύω', 'AAI.1S'))
defaultdict(<class 'list'>,
            {'ἔλυσα': [{'accent_notes': 'recessive (default)',
                        'original_form': 'ελυσα',
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
 ('PMI.1S', 'ποιου{athematic}'),
 ('XMI.1S', 'ποιου'),
 ('ZMI.1S', 'ποι{contract}')]

Notice that the system doesn't yet have any heuristics around likely stem
shape.

You can pass an optional regex to ``possible_stems`` if you have an idea of the
parsing:

>>> pprint.pprint(sorted(inflexion.possible_stems('ποιοῦμαι', '.+1S$')))
[('FMI.1S', 'ποι{contract}'),
 ('PMI.1S', 'ποιε'),
 ('PMI.1S', 'ποιο'),
 ('PMI.1S', 'ποιου{athematic}'),
 ('XMI.1S', 'ποιου'),
 ('ZMI.1S', 'ποι{contract}')]


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

>>> inflexion.conjugate_core("λύω", "PAI", "AAI", tags={"final-nu-aai.3s"})
[('PAI', {'PAI.1S': 'λῡ́ω', 'PAI.2S': 'λῡ́εις', 'PAI.3S': 'λῡ́ει', 'PAI.1P': 'λῡ́ομεν', 'PAI.2P': 'λῡ́ετε', 'PAI.3P': 'λῡ́ουσι(ν)'}), ('AAI', {'AAI.1S': 'ἔλυσα', 'AAI.2S': 'ἔλυσας', 'AAI.3S': 'ἔλυσε(ν)', 'AAI.1P': 'ἐλύσαμεν', 'AAI.2P': 'ἐλύσατε', 'AAI.3P': 'ἔλυσαν'})]

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
    PAP.NSF: λῡ́ουσᾰ
    PAP.GSF: λῡούσης
    PAP.DSF: λῡούσῃ
    PAP.ASF: λῡ́ουσᾰν
    PAP.VSF: λῡ́ουσᾰ
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

# `paradigm_tools.py`

`paradigm_tools.py` defines a few functions that use `greek-inflexion` to generate paradigms in either `html` or `markdown`.

For verbs use:

* `conjugate_html`
* `conjugate_md`




>>> import paradigm_tools as pu


>>> pu.conjugate_md("λύω", "PAI", "PMI", tags={"final-nu-aai.3s"}, merge_paradigms=True)
| ἀριθμός | πρώσοπον | ἐνεστώς ἐνεργητικόν ὁριστική | ἐνεστώς μέσον ὁριστική |
|:----|:----|:----|:----|
| ἑνικόν | πρῶτον | λῡ́ω | λῡ́ομαι |
| | δευτέρον | λῡ́εις | λῡ́ῃ/λῡ́ει |
| | τρίτον | λῡ́ει | λῡ́εται |
| πληθυντικόν | πρῶτον | λῡ́ομεν | λῡόμεθα |
| | δευτέρον | λῡ́ετε | λῡ́εσθε |
| | τρίτον | λῡ́ουσι(ν) | λῡ́ονται |
<BLANKLINE>

>>> pu.conjugate_md("λύω", "PAI", "PMI", tags={"final-nu-aai.3s"}, merge_paradigms=False)
| ἀριθμός | πρώσοπον | ἐνεστώς ἐνεργητικόν ὁριστική |
|:----|:----|:----|
| ἑνικόν | πρῶτον | λῡ́ω |
| | δευτέρον | λῡ́εις |
| | τρίτον | λῡ́ει |
| πληθυντικόν | πρῶτον | λῡ́ομεν |
| | δευτέρον | λῡ́ετε |
| | τρίτον | λῡ́ουσι(ν) |
<BLANKLINE>
| ἀριθμός | πρώσοπον | ἐνεστώς μέσον ὁριστική |
|:----|:----|:----|
| ἑνικόν | πρῶτον | λῡ́ομαι |
| | δευτέρον | λῡ́ῃ/λῡ́ει |
| | τρίτον | λῡ́εται |
| πληθυντικόν | πρῶτον | λῡόμεθα |
| | δευτέρον | λῡ́εσθε |
| | τρίτον | λῡ́ονται |
<BLANKLINE>

>>> pu.conjugate_html("λύω", "PAN", "AAN", tags={"final-nu-aai.3s"})
<link href="./paradigm.css" rel="stylesheet">
<table class="verb-paradigm">
<thead><tr class="para-header-row"><td class="para-header-cell"></td><td class="para-header-cell">ἀπαρέμφατος</td></tr></thead><tbody>
<tr><td class="para-item">ἐνεστώς ἐνεργητικόν</td><td class="para-item">λῡ́ειν</td></tr>
<tr><td class="para-item">ἀόριστος ἐνεργητικόν</td><td class="para-item">λῦσαι</td></tr>
</tbody>
</table>
<BLANKLINE>

For participels, adjectives, and nouns use:

* `decline_html`
* `decline_md`


>>> pu.decline_md("λύω", "PAP")
|  ἀριθμός | πτῶσις | ἀρσενικόν | θηλυκόν | οὐδέτερον  |
|:----|:----|:----|:----|:----|
| ἑνικόν | ὀνομαστική | λῡ́ων | λῡ́ουσᾰ | λῦον |
| | γενική | λῡ́οντος | λῡούσης | λῡ́οντος |
| | δοτική | λῡ́οντι | λῡούσῃ | λῡ́οντι |
| | αἰτιατική | λῡ́οντα | λῡ́ουσᾰν | λῦον |
| | κλητική | λῡ́ων | λῡ́ουσᾰ | λῦον |
| πληθυντικόν | ὀνομαστική | λῡ́οντες | λῡ́ουσαι | λῡ́οντα |
| | γενική | λῡόντων | λῡουσῶν | λῡόντων |
| | δοτική | λῡ́ουσι(ν) | λῡούσαις | λῡ́ουσι(ν) |
| | αἰτιατική | λῡ́οντας | λῡούσᾱς | λῡ́οντα |
| | κλητική | λῡ́οντες | λῡ́ουσαι | λῡ́οντα |
<BLANKLINE>


In cases where one does not want to use the forms found by `greek-inflexion` the following code can be run. If you want a merged paradigm where all forms are combined in the same table, then run the code below. It expects a list containing the lists for forms to be displayed and a list of column headers for each list. There is also a markdown version of this function called `layout_merged_verb_paradigm_md`. If you want seperate tables for each list, then run `layout_non_merged_verb_paradigm_html` or `layout_non_merged_verb_paradigm_md`. **Note**: this only work for indicative, subjuncitve, and optative.


>>> labels = pu.load_labels("labels.yaml", 'el')
>>> pu.layout_merged_verb_paradigm_html([["1", "2", "3", "4", "5", "6"]], ["Random"], labels)
<link href="./paradigm.css" rel="stylesheet">
<table class="verb-paradigm">
<thead><tr class="para-header-row"><td class="para-header-cell">ἀριθμός</td><td class="para-header-cell">πρώσοπον</td><td class="para-header-cell"></td></tr></thead><tbody>
<tr><td class="para-row-label" rowspan="3" valign="top">ἑνικόν</td><td class="para-row-label">πρῶτον</td><td class="para-item">1</td></tr>
<tr><td class="para-row-label">δευτέρον</td><td class="para-item">2</td></tr>
<tr><td class="para-row-label">τρίτον</td><td class="para-item">3</td></tr>
<tr><td class="para-row-label" rowspan="3" valign="top">πληθυντικόν</td><td class="para-row-label">πρῶτον</td><td class="para-item">4</td></tr>
<tr><td class="para-row-label">δευτέρον</td><td class="para-item">5</td></tr>
<tr><td class="para-row-label">τρίτον</td><td class="para-item">6</td></tr>
</tbody>
</table>
<BLANKLINE>


If you want seperate tables for each list, then run `layout_non_merged_verb_paradigm_html` or `layout_non_merged_verb_paradigm_md`. Note that unlike the merged versions, it expects a list of the forms (rather than a list of lists) and a single label (rather than a list of labels).


>>> pu.layout_non_merged_verb_paradigm_md(["1", "2", "3", "4", "5", "6"], "Random", labels)
| ἀριθμός | πρώσοπον |  |
|:----|:----|:----|
| ἑνικόν | πρῶτον | 1 |
| | δευτέρον | 2 |
| | τρίτον | 3 |
| πληθυντικόν | πρῶτον | 4 |
| | δευτέρον | 5 |
| | τρίτον | 6 |
<BLANKLINE>
