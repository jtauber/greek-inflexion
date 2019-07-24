PARTS = {
    "1-": [
        "PAI", "PAD", "PAN", "PAP", "PAS", "PAO",
        "PMI", "PMD", "PMN", "PMP", "PMS", "PMO",
    ],
    "1+": [
        "IAI",
        "IMI",
        "IEI",
    ],
    "2-": [
        "FAI", "FAN", "FAP", "FAO",
        "FMI", "FMN", "FMP", "FMO",
    ],
    "3-": [
        "AAD", "AAN", "AAP", "AAS", "AAO",
        "AMD", "AMN", "AMP", "AMS", "AMO",
    ],
    "3+": [
        "AAI",
        "AMI",
    ],
    "4-": [
        "XAI", "XAD", "XAN", "XAP", "XAS", "XAO",
    ],
    "4+": [
        "YAI",
    ],
    "5-": [
        "XMI", "XMD", "XMN", "XMP",
    ],
    "5+": [
        "YMI", "YMP",
    ],
    "6-": [
        "APD", "APN", "APP", "APS", "APO",
    ],
    "6+": [
        "API",
    ],
    "7-": [
        "FPI", "FPN", "FPP", "FPO",
    ],
    "8-": [
        "ZAI", "ZAN",
        "ZMI",
    ],
}

REVERSE_PARTS = {}

for part, tvm_list in PARTS.items():
    for tvm in tvm_list:
        REVERSE_PARTS[tvm] = part


def key_to_part(key):
    return REVERSE_PARTS[key[0:3]]


def trim_multiples(stem_set, part, lemma, parts):
    trimmed_stems = set()
    for stem in stem_set:
        if stem.endswith("0"):  # rarely a real stem
            pass
        elif stem.endswith("@"):  # rarely a real stem
            pass
        elif part[0] == "3" and lemma.endswith(("άω", "έω", "όω", "εύω")) and \
                stem.endswith(("{root}", "{athematic}", "{2nd}")):
            pass
        elif lemma.endswith(("ω", "ομαι")) and stem.endswith("{athematic}"):
            pass
        elif part[0] == "1" and lemma.endswith("έω") and \
                stem.endswith(("ο", "α", "η")):
            pass
        elif part[0] == "1" and lemma.endswith("όω") and \
                stem.endswith(("ε", "α", "η", "{athematic}")):
            pass
        elif part[0] == "1" and lemma.endswith("άω") and \
                stem.endswith(("η", "ε", "ο")):
            pass
        elif part[0] == "1" and lemma.endswith("έομαι") and stem.endswith("ο"):
            pass
        elif part[0] == "1" and lemma.endswith("όομαι") and stem.endswith("ε"):
            pass
        elif part[0] == "1" and lemma.endswith("άομαι") and stem.endswith("η"):
            pass
        else:
            trimmed_stems.add(stem)

    if part == "3-" and len(stem_set) == 2:
        t = sorted(stem_set)
        if t[0] + "{2nd}" == t[1]:
            return "{}  # @1 2nd?".format(t[0])
        if t[1].endswith("ι{2nd}") and t[1] == t[0][:-5] + "ι{2nd}":
            return "{}  # @1".format(t[0])

    if len(trimmed_stems) == 1:
        return "{}  # @1".format(trimmed_stems.pop())
    elif len(trimmed_stems) == 0:
        return "{}  # @mm".format(stem_set)
    else:
        return "{}  # @m".format("/".join(trimmed_stems))
