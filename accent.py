import re

from greek_accentuation.characters import accent, strip_length
from greek_accentuation.characters import strip_accents  # noqa
from greek_accentuation.syllabify import rebreath
from greek_accentuation.syllabify import debreath  # noqa
from greek_accentuation.accentuation import (
    recessive, persistent, on_penult, make_oxytone)


def clean(w):
    return rebreath(w).replace("|", "")


def calculate_accent(w, parse, lemma, stem, inflexion, accent_override):
    if accent(w):
        # explicit
        return clean(w)
    elif list(stem)[0].endswith("{enclitic}"):
        # enclitic
        return clean(make_oxytone(w))
    elif len(parse) == 3 and parse[2] != "N":  # nominal
        base_accent = None
        for key_regex, accented in accent_override.get(lemma, []):
            if re.match(key_regex, parse):
                base_accent = accented
                break
        if base_accent:
            return clean(persistent(w, base_accent))
        else:
            return clean(persistent(w, lemma))
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
