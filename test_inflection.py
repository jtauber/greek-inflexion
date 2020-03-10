from greek_inflexion import GreekInflexion
import pprint

inflexion = GreekInflexion('stemming.yaml', 'STEM_DATA/pratt_lexicon.yaml')


import paradigm_tools as pu

#print(inflexion.conjugate_core("λύω", "PAI", "AAI", tags={"final-nu-aai.3s"}))

#print()

labels = pu.load_labels("labels.yaml", "el")

#pu.decline_html("λύω", "PAP")
#pu.decline_md("λύω", "PAP")

#pu.conjugate_html("λύω", "PAD", "AAD", tags={"final-nu-aai.3s"}, merge_paradigms=False)
pu.conjugate_html("λύω", "PAI", "AAI", tags={"final-nu-aai.3s"})


exit()

pu.conjugate_html("λύω", "PAI", "PMI", "FAI", "FMI", tags={"final-nu-aai.3s"})

pu.conjugate_html("λύω", "PAI", "PMI", tags={"final-nu-aai.3s"}, merge_paradigms=False)

pu.layout_merged_verb_paradigm_html([["1", "2", "3", "4", "5", "6"]], ["Random"], labels)

pu.layout_merged_verb_paradigm_md([["1", "2", "3", "4", "5", "6"]], ["Random"], labels)

pu.layout_non_merged_verb_paradigm_md(["1", "2", "3", "4", "5", "6"], "Random", labels)
pu.conjugate_md("λύω", "PAI", "PMI", tags={"final-nu-aai.3s"}, merge_paradigms=True)
pu.conjugate_md("λύω", "PAI", "PMI", tags={"final-nu-aai.3s"}, merge_paradigms=False)
