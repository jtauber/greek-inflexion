import re

from greek_accentuation.characters import accent, strip_length
from greek_accentuation.characters import strip_accents  # noqa
from greek_accentuation.syllabify import rebreath
from greek_accentuation.syllabify import debreath  # noqa
from greek_accentuation.accentuation import (
    recessive, persistent, on_penult, make_oxytone)


def clean(w):
    return rebreath(w).replace("|", "").replace("-", "")


def calculate_accent(w, parse, lemma, segmented_lemma, stem, inflexion,
                     accent_override):
    if accent(w):
        # explicit
        return clean(w), "explicit"
    elif list(stem)[0].endswith("{enclitic}"):
        # enclitic
        return clean(make_oxytone(w)), "enclitic"
    elif len(parse) == 3 and parse[2] != "N":  # nominal
        base_accent = None
        for key_regex, accented in accent_override.get(lemma, []):
            if re.match(key_regex, parse):
                base_accent = accented
                break
        if base_accent:
            return (
                clean(persistent(w, base_accent)),
                "nominal: persistent from override {}".format(base_accent)
            )
        else:
            return (
                clean(persistent(w, lemma)),
                "nominal: persistent from lemma"
            )
    else:
        if parse[2] == "P":
            base_accent = None
            for key_regex, accented in accent_override.get(lemma, []):
                if re.match(key_regex, parse):
                    base_accent = accented
                    break
            if base_accent:
                return (
                    clean(persistent(w, base_accent)),
                    f"participle: persistent from override {base_accent}"
                )
            elif parse == "AAP.NSM" and w.endswith("ων"):
                return (
                    clean(make_oxytone(w)),
                    "participle: AAP.NSM -ων oxytone"
                )
            elif parse == "PAP.NSM" and w.endswith("ς"):
                return (
                    clean(make_oxytone(w)),
                    "participle: PAP.NSM -ς oxtyone"
                )
            elif parse[0:3] == "AAP" and parse != "AAP.NSM":
                # calculate NSM
                nsms = [
                    calculate_accent(
                        w, "AAP.NSM", lemma, segmented_lemma, stem, inflexion,
                        accent_override
                    ) for w in inflexion.generate(lemma, "AAP.NSM")
                ]
                for nsm, _ in nsms:
                    if nsm.endswith(("ών", "ούς")):
                        # persistent participle (based on nsm)
                        return (
                            clean(persistent(w, nsm, default_short=True)),
                            f"participle: AAP persistent from NSM {nsm}"
                        )
                    else:
                        # persistent participle (based on lemma)
                        if "-" in w:
                            pre, rest = w.split("-")
                            lemma_pre, lemma_rest = segmented_lemma.split("-")
                            return (
                                clean(
                                    pre + persistent(
                                        rest, lemma_rest, default_short=True)),
                                "participle: AAP persistent"
                                " from lemma (using segmentation)"
                            )
                        else:
                            return (
                                clean(
                                    persistent(w, lemma, default_short=True)),
                                "participle: AAP persistent from lemma"
                            )
            elif parse[0:3] == "PAP" and parse != "PAP.NSM":
                # calculate NSM
                nsms = [
                    calculate_accent(
                        w, "PAP.NSM", lemma, segmented_lemma, stem, inflexion,
                        accent_override
                    ) for w in inflexion.generate(lemma, "PAP.NSM")
                ]

                for nsm, _ in nsms:
                    nsm = strip_length(nsm)
                    return (
                        clean(persistent(w, nsm, default_short=True)),
                        f"participle: PAP persistent from NSM {nsm}"
                    )
            else:
                return (
                    clean(recessive(w, default_short=True)),
                    "participle: recessive"
                )
        elif parse[0:3] in ["AAN", "XAN", "XMN", "XPN"]:
            return (
                clean(on_penult(w, default_short=True)),
                "infinitive: AAN XAN XMN XPN penult"
            )
        elif parse[0:3] == "PAN" and stem.endswith("{athematic}"):
            return (
                clean(on_penult(w, default_short=True)),
                "infinitive: PAN athematic penult"
            )
        elif parse[0:3] == "AMN" and stem.endswith(
                ("{root}", "{athematic}", "{2nd}")):
            return (
                clean(on_penult(w, default_short=True)),
                "infinitive: AMN root/2nd penult"
            )
        elif parse[2] == "O":
            return (
                clean(recessive(
                    w, treat_final_AI_OI_short=False, default_short=True)),
                "optative: recessive"
            )
        else:
            return (
                clean(recessive(w, default_short=True)),
                "recessive (default)"
            )
