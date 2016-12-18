# -*- coding: utf-8 -*-

import unicodedata

VARIA = u"\u0300"
OXIA = u"\u0301"
PSILI = u"\u0313"
DASIA = u"\u0314"
PERISPOMENI = u"\u0342"

ACCENTS = [VARIA, OXIA, PERISPOMENI]


def d(s):
    return unicodedata.normalize("NFD", s)


def n(x):
    return unicodedata.normalize("NFKC", x)


def strip_accents(s):
    return ''.join((c for c in d(s) if unicodedata.category(c) != "Mn"))


def count_accents(s):
    count = 0
    for c in d(s):
        if c in ACCENTS:
            count += 1
    return count


def strip_last_accent(word):
    x = list(word)
    for i, ch in enumerate(x[::-1]):
        s = strip_accents(ch)
        if s != ch:
            x[-i - 1] = s
            break
    return u"".join(x)


CLITICS = [
    u"εἰμί",
    u"εἰσίν",
    u"ἐσμέν",
    u"ἐστέ",
    u"γέ",
    u"ποτέ",
    u"τέ",
    u"φησίν",
    u"πώς",
    u"ποῦ",
    u"φημί",
]

clitics_dict = {}
for word in CLITICS:
    clitics_dict[strip_last_accent(word)] = word


def convert(word, lemma, parse):
    norm = word

    # change graves to acutes
    temp = ""
    for ch in d(norm):
        if ch == VARIA:
            ch = OXIA  # OXIA will be normalized to TONOS below if needed
        temp += ch
    norm = n(temp)

    if count_accents(norm) == 2:
        norm = strip_last_accent(norm)
        assert count_accents(norm) == 1

    # # normalize movable nu in 3rd person verb
    if parse in ["AAI.3S", "IAI.3S", "XAI.3S"]:
        if norm.endswith(u"εν"):
            norm = norm[:-1] + u"(ν)"
        if norm.endswith(u"ε"):
            norm = norm + u"(ν)"
    if parse in ["YAI.3S"]:
        if norm.endswith(u"ειν"):
            norm = norm[:-1] + u"(ν)"
        if norm.endswith(u"ει"):
            norm = norm + u"(ν)"

    if count_accents(norm) == 0:
        if norm in clitics_dict:
            norm = clitics_dict[norm]

    if parse[4:] in ["3S", "3P", "DPM"]:
        if (
            norm.endswith(u"σιν") or
            norm.endswith(u"σίν") or
            norm.endswith(u"ξίν") or
            norm.endswith(u"ξιν")
        ):
            norm = norm[:-1] + u"(ν)"
        if (
            norm.endswith(u"σι") or
            norm.endswith(u"σί") or
            norm.endswith(u"ξί")
        ):
            norm = norm + u"(ν)"

    if norm in [u"ἐστιν", u"ἐστίν", u"ἐστι", u"ἐστί", u"ἔστιν", u"ἔστι"]:
        norm = u"ἐστί(ν)"

    # if norm in [u"ἔξεστιν", u"ἔξεστι"]:
    #     norm = u"ἔξεστι(ν)"

    # if norm == u"πάρεστιν":
    #     norm = u"πάρεστι(ν)"

    return norm
