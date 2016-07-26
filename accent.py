import re

from characters import accent, strip_length, remove_diacritic
from characters import strip_accents  # noqa
from characters import SMOOTH
from characters import remove_redundant_macron
from accentuation import recessive, persistent, on_penult, make_oxytone
from syllabify import add_necessary_breathing

remove_smooth_breathing = remove_diacritic(SMOOTH)


# @@@ move to greek-accentuation eventually
def debreath(word):
    word = remove_smooth_breathing(word)
    word = word.replace("εἷ", "hεῖ")
    word = word.replace("εἵ", "hεί")
    word = word.replace("εἱ", "hει")
    word = word.replace("ἕ", "hέ")
    word = word.replace("ἑ", "hε")

    return word


# @@@ move to greek-accentuation eventually
def rebreath(word):
    if word == "":
        return word
    word = word.replace("hεῖ", "εἷ")
    word = word.replace("hεί", "εἵ")
    word = word.replace("hει", "εἱ")
    word = word.replace("hέ", "ἕ")
    word = word.replace("hε", "ἑ")
    word = word.replace("hῇ", "ᾗ")
    word = word.replace("hῶ", "ὧ")
    word = word.replace("hῆ", "ἧ")
    word = word.replace("hοῦ", "οὗ")
    word = word.replace("hώ", "ὥ")
    word = add_necessary_breathing(word)
    word = remove_redundant_macron(word)

    return word


def clean(w):
    return rebreath(w).replace("|", "")


def calculate_accent(w, parse, lemma, stem, inflexion, accent_override):
    if accent(w):
        # explicit
        return clean(w)
    elif list(stem)[0].endswith("{enclitic}"):
        # enclitic
        return clean(make_oxytone(w))
    else:
        if parse[2] == "P":
            base_accent = None
            for key_regex, accented in accent_override.get(lemma, []):
                if re.match(key_regex, parse):
                    base_accent = accented
                    break
            if base_accent:
                # persistent participle
                return clean(persistent(w, base_accent))
            elif parse == "AAP.NSM" and w.endswith("ων"):
                # aap.nsm oxytone
                return clean(make_oxytone(w))
            elif parse == "PAP.NSM" and w.endswith("ς"):
                # pap.nsm oxytone"
                return clean(make_oxytone(w))
            elif parse[0:3] == "AAP" and parse != "AAP.NSM":
                # calculate NSM
                nsms = [
                    calculate_accent(
                        w, "AAP.NSM", lemma, stem, inflexion, accent_override)
                    for w in inflexion.generate(lemma, "AAP.NSM")
                ]
                for nsm in nsms:
                    if nsm.endswith(("ών", "ούς")):
                        # persistent participle (based on nsm)
                        return clean(persistent(w, nsm))
                    else:
                        # persistent participle (based on lemma)
                        return clean(persistent(w, lemma))
            elif parse[0:3] == "PAP" and parse != "PAP.NSM":
                # calculate NSM
                nsms = [
                    calculate_accent(
                        w, "PAP.NSM", lemma, stem, inflexion, accent_override)
                    for w in inflexion.generate(lemma, "PAP.NSM")
                ]

                for nsm in nsms:
                    nsm = strip_length(nsm)
                    return clean(persistent(w, nsm))
            else:
                return clean(recessive(w, default_short=True))
        elif parse[0:3] in ["AAN", "XAN", "XMN", "XPN"]:
            # inf.penult
            return clean(on_penult(w, default_short=True))
        elif parse[0:3] == "PAN" and list(stem)[0].endswith("!"):
            # athematic present inf. penult
            return clean(on_penult(w, default_short=True))
        elif parse[2] == "O":
            # recessive (optative)
            return clean(recessive(
                w, treat_final_AI_OI_short=False, default_short=True))
        else:
            # recessive (default)
            return clean(recessive(w, default_short=True))
