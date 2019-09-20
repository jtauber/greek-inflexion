#!/usr/bin/env python3

import sys

from greek_inflexion import GreekInflexion

mi = GreekInflexion("stemming.yaml", "STEM_DATA/morphgnt_lexicon.yaml")


incorrect_count = 0


def test(ref, inflexion, lemma, key, expected):
    global incorrect_count
    result = set(inflexion.generate(lemma, key))
    if result != expected:
        print(f"failed {ref} {lemma} {key} {expected} (got {result}))")
        incorrect_count += 1


test("#3", mi, "ἀνίστημι", "AMD.2S", {"ἀνάστησαι"})
test("#3", mi, "ἀνίστημι", "AMD.3S", {"ἀναστησάσθω"})
test("#3", mi, "ἀνίστημι", "AMD.2P", {"ἀναστήσασθε"})
test("#3", mi, "ἀνίστημι", "AMD.3P", {"ἀναστησάσθων"})

test("#29", mi, "δίδωμι", "PAP.DPF", {"διδούσαις"})

test("#30", mi, "τίθημι", "AAS.3P", {"θῶσι(ν)", "θήσωσι(ν)"})
test("#30", mi, "τίθημι", "AMP.APF", {"θεμένᾱς", "θησαμένᾱς"})
test("#30", mi, "τίθημι", "AMP.APM", {"θεμένους", "θησαμένους"})
test("#30", mi, "τίθημι", "AMP.APN", {"θέμενα", "θησάμενα"})
test("#30", mi, "τίθημι", "AMP.ASF", {"θεμένην", "θησαμένην"})
test("#30", mi, "τίθημι", "AMP.DPF", {"θεμέναις", "θησαμέναις"})
test("#30", mi, "τίθημι", "AMP.DPM", {"θεμένοις", "θησαμένοις"})


if incorrect_count > 0:
    sys.exit(1)
