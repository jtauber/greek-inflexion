from unicodedata import normalize

from greekutils.beta2unicode import convert


book_to_num = {
    "Gen": 1,
    "Exod": 3,
    "Lev": 4,
    "Num": 5,
    "Deut": 6,
    "JoshB": 7,
    "JoshA": 8,
    "2Esdr": 19,
    "1Mac": 24,
    "Jonah": 42,
    "Nah": 44,
}


def convert_parse(parse):
    if parse[2] in "DISOP":
        result = parse[:3] + "." + parse[3:]
    elif parse[2] in "N":
        result = parse
    if result[1] == "P" and result[0] not in "AF":
        result = result[0] + "M" + result[2:]
    return result


def get_words(filename):

    state = 0

    with open(filename) as f:
        for line in f:
            s = line.strip()
            if state == 0:  # expecting verse ref
                b, cv = s.split()
                c, v = cv.split(":")
                if v[-1] in "abcdef":  # @@@
                    v = v[:-1]
                else:
                    w = 0
                state = 1
            elif state == 1:    # expecting word line or blank link
                if s:
                    w += 1
                    if s[25] == "V":  # verb
                        yield {
                            "line": s,
                            "ref": "{:02d}.{:03d}.{:03d}.{:03d}".format(
                                book_to_num[b], int(c), int(v), w),
                            "word": normalize(
                                "NFKC", convert(s[:25].strip() + " ").strip()),
                            "type": s[25:28].strip(),
                            "parse": s[29:35].strip(),
                            "lemma": normalize(
                                "NFKC", convert(
                                    s[36:52].strip() + " ").strip()),
                            "preverb": normalize(
                                "NFKC", convert(s[53:].strip() + " ").strip()),
                        }
                else:
                    state = 0  # blank link so back to expecting verse ref


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
        return "{}  # @m".format(trimmed_stems)
