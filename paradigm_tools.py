# py -m doctest -v examples.rst
from greek_inflexion import GreekInflexion
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

inflexion = GreekInflexion('stemming.yaml', 'STEM_DATA/pratt_lexicon.yaml')


def rotate_lists(xs):
    len_x0 = len(xs[0])
    for x in xs:
        assert len(x) == len_x0
    out = []
    for i in range(0,len(xs[0])):
        out.append([x[i] for x in xs])
    return out


def load_labels(fpath, lang):
    with open(fpath, 'r', encoding="UTF-8") as f:
        labels = load(f, Loader=Loader)
        return labels[lang]


def layout_merged_imp_paradigm_md(verbs, TVMs, labels):
    verbs = [[f' {y} ' for y in xs] for xs in verbs]
    row_labels = [f' {labels[x]} ' for x in ['2nd', '3rd']] * 2
    verbs.insert(0,row_labels)
    sgpl = [f' {labels["SG"]} ', ' ', f' {labels["PL"]} ' , ' ']
    verbs.insert(0,sgpl)
    header = [f' {labels["number"]} ', f' {labels["person"]} ']
    header.extend([f' {labels[x]} ' if x in labels else f' {labels["unknown"]} ' for x in TVMs])
    r_verbs = rotate_lists(verbs)
    tcontent = "|" + "|".join(header) + "|\n"
    tcontent += "|" + ":----|" * len(header) + "\n"
    tcontent += "\n".join(['|' + "|".join(x) + '|' for x in r_verbs])
    print(tcontent)
    print()


def layout_non_merged_imp_paradigm_md(verbs, tvm, labels):
    row_labels = [f' {labels[x]} ' for x in ['2nd', '3rd']] * 2
    v = [f' {y} ' for y in verbs]
    header = [f' {labels["number"]} ',
             f' {labels["person"]} ',
             f' {labels[tvm] if tvm in labels else labels["unknown"]} ']
    numbers = [f' {labels["SG"]} ', ' ', f' {labels["PL"]} ', ' ']
    r_verbs = rotate_lists([numbers, row_labels, v])
    tcontent = "|" + "|".join(header) + "|\n"
    tcontent += "|:----|:----|:----|\n"
    tcontent += "\n".join(['|' + "|".join(x) + '|' for x in r_verbs])
    print(tcontent)
    print()


def layout_merged_verb_paradigm_md(verbs, TVMs, labels):
    verbs = [[f' {y} ' for y in xs] for xs in verbs]
    row_labels = [f' {labels[x]} ' for x in ['1st', '2nd', '3rd']] * 2
    verbs.insert(0,row_labels)
    sgpl = [f' {labels["SG"]} ', ' ', ' ', f' {labels["PL"]} ' , ' ' , ' ']
    verbs.insert(0,sgpl)
    header = [f' {labels["number"]} ', f' {labels["person"]} ']
    header.extend([f' {labels[x]} ' if x in labels else f' {labels["unknown"]} ' for x in TVMs])
    r_verbs = rotate_lists(verbs)
    tcontent = "|" + "|".join(header) + "|\n"
    tcontent += "|" + ":----|" * len(header) + "\n"
    tcontent += "\n".join(['|' + "|".join(x) + '|' for x in r_verbs])
    print(tcontent)
    print()


def layout_non_merged_verb_paradigm_md(verbs, tvm, labels):
    row_labels = [f' {labels[x]} ' for x in ['1st', '2nd', '3rd']] * 2
    v = [f' {y} ' for y in verbs]
    header = [f' {labels["number"]} ',
             f' {labels["person"]} ',
             f' {labels[tvm] if tvm in labels else labels["unknown"]} ']
    numbers = [f' {labels["SG"]} ', ' ', ' ', f' {labels["PL"]} ' , ' ' , ' ']
    r_verbs = rotate_lists([numbers, row_labels, v])
    tcontent = "|" + "|".join(header) + "|\n"
    tcontent += "|:----|:----|:----|\n"
    tcontent += "\n".join(['|' + "|".join(x) + '|' for x in r_verbs])
    print(tcontent)
    print()


def layout_merged_inf_paradigm_md(forms, labels):
    print("| | " + labels["inf"] + " |")
    print("|:---|:---|")
    for tvm, form in forms:
        print(f'| {labels[tvm] if tvm in labels else labels["unknown"]} | {form[0]} |')
    print()


def layout_non_merged_inf_paradigm_md(form, tvm, labels):
    print("| | " + labels["inf"] + " |")
    print("|:---|:---|")
    print(f'| {labels[tvm] if tvm in labels else labels["unknown"]} | {form[0]} |')
    print()


def layout_participle_summary_paradigm_md(forms, label, labels):
    forms = [f' {x} ' for x in forms]
    header = [f' {labels["number"]} ',
             f' {labels["case"]} ',
             f' {labels["masc"]} ',
             f' {labels["fem"]} ',
             f' {labels["neut"]} ']
    cases =  [f' {labels["nom"]} ',
               f' {labels["gen"]} '] * 2
    row1 = forms[0:3]
    row2 = forms[3:]
    row1.insert(0, f' {labels["nom"]} ')
    row1.insert(0, f' {labels["SG"]} ')
    row2.insert(0, f' {labels["gen"]} ')
    row2.insert(0, f' ')
    rows = [row1, row2]
    tcontent = f'| {"|".join(header)} |\n'
    tcontent += f'|:-----|:-----|:-----|:-----|:-----|\n'
    tcontent += "\n".join([f'| {"|".join(x)} |' for x in rows])
    print(tcontent)
    print()


def conjugate_md(lemma, *TVMs, tags=None, labels="labels.yaml", lang="el", merge_paradigms=True):
    labels = load_labels(labels, lang)
    forms = inflexion.conjugate_core(lemma, *TVMs, tags=tags)
    # participles can't be merged with other verb paradigms
    verbs = [(fs[0], list(fs[1].values())) for fs in forms if fs[0][2] in "SOI"]
    imps = [(fs[0], list(fs[1].values())) for fs in forms if fs[0][2] == "D"]
    infs = [(fs[0], list(fs[1].values())) for fs in forms if fs[0][2] == "N"]
    parts = [(fs[0], list(fs[1].values())) for fs in forms if fs[0][2] == "P"]
    if verbs:
        if merge_paradigms:
            tvms = [x[0] for x in verbs]
            verbs = [x[1] for x in verbs]
            layout_merged_verb_paradigm_md(verbs, tvms, labels)
        else:
            for label, v in verbs:
                layout_non_merged_verb_paradigm_md(v, label, labels)
    if infs:
        if merge_paradigms:
            layout_merged_inf_paradigm_md(infs, labels)
        else:
            for label, v in infs:
                layout_non_merged_inf_paradigm_md(v, label, labels)
    if imps:
        if merge_paradigms:
            tvms = [x[0] for x in imps]
            imps = [x[1] for x in imps]
            layout_merged_imp_paradigm_md(imps, tvms, labels)
        else:
            for label, v in imps:
                layout_non_merged_imp_paradigm_md(v, label, labels)
    if parts:
        for label, v in parts:
            layout_participle_summary_paradigm_md(v, label, labels)


def layout_merged_imp_paradigm_html(verbs, TVMs, labels):
    verbs = [[f'<td class="para-item">{y}</td>' for y in xs] for xs in verbs]
    row_labels = [f'<td class="para-row-label">{labels[x]}</td>' for x in ['2nd', '3rd']] * 2
    verbs.insert(0,row_labels)
    header = [f'<td class="para-header-cell">{labels[x]}</td>' if x in labels else f'<td class="para-header-cell">{labels["unknown"]}</td>' for x in TVMs]
    header.insert(0, f'<td class="para-header-cell">{labels["person"]}</td>')
    header.insert(0, f'<td class="para-header-cell">{labels["number"]}</td>')
    r_verbs = rotate_lists(verbs)
    r_verbs[0].insert(0, f'<td class="para-row-label" rowspan="2" valign="top">{labels["SG"]}</td>')
    r_verbs[2].insert(0, f'<td class="para-row-label" rowspan="2" valign="top">{labels["PL"]}</td>')
    tcontent = f'<thead><tr class="para-header-row">{"".join(header)}</tr></thead>'
    tcontent += "<tbody>\n" + "\n".join([f'<tr>{"".join(x)}</tr>' for x in r_verbs]) + "\n</tbody>"
    print("<link href=\"./paradigm.css\" rel=\"stylesheet\">")
    print(f'<table class="verb-paradigm">\n{tcontent}\n</table>')
    print()


def layout_non_merged_imp_paradigm_html(verbs, tvm, labels):
    row_labels = [f'<td class="para-row-label">{labels[x]}</td>' for x in ['2nd', '3rd']] * 2
    v = [f'<td class="para-item">{y}</td>' for y in verbs]
    header = [f'<td class="para-header-cell">{labels["number"]}</td>',
             f'<td class="para-header-cell">{labels["person"]}</td>',
             f'<td class="para-header-cell">{labels[tvm]}</td>' if tvm in labels else f'<td class="para-header-cell">{labels["unknown"]}</td>']
    r_verbs = rotate_lists([row_labels, v])
    r_verbs[0].insert(0, f'<td class="para-row-label" rowspan="2" valign="top">{labels["SG"]}</td>')
    r_verbs[2].insert(0, f'<td class="para-row-label" rowspan="2" valign="top">{labels["PL"]}</td>')
    tcontent = f'<thead><tr class="para-header-row">{"".join(header)}</tr></thead>'
    tcontent += "<tbody>\n" + "\n".join([f'<tr>{"".join(x)}</tr>' for x in r_verbs]) + "\n</tbody>"
    print("<link href=\"./paradigm.css\" rel=\"stylesheet\">")
    print(f'<table class="verb-paradigm">\n{tcontent}\n</table>')
    print()


def layout_merged_inf_paradigm_html(verbs, labels):
    header = [f'<td class="para-header-cell"></td>',
             f'<td class="para-header-cell">{labels["inf"]}</td>']
    vs = [[f'<td class="para-item">{labels[tvm] if tvm in labels else labels["unknown"]}</td>',
            f'<td class="para-item">{y[0]}</td>'] for (tvm, y) in verbs]
    tcontent = f'<thead><tr class="para-header-row">{"".join(header)}</tr></thead>'
    tcontent += "<tbody>\n" + "\n".join([f'<tr>{"".join(x)}</tr>' for x in vs]) + "\n</tbody>"
    print("<link href=\"./paradigm.css\" rel=\"stylesheet\">")
    print(f'<table class="verb-paradigm">\n{tcontent}\n</table>')
    print()


def layout_non_merged_inf_paradigm_html(verbs, tvm, labels):
    header = [f'<td class="para-header-cell"></td>',
             f'<td class="para-header-cell">{labels["inf"]}</td>']
    vs = [[f'<td class="para-item">{labels[tvm] if tvm in labels else labels["unknown"]}</td>',
            f'<td class="para-item">{y}</td>'] for y in verbs]
    tcontent = f'<thead><tr class="para-header-row">{"".join(header)}</tr></thead>'
    tcontent += "<tbody>\n" + "\n".join([f'<tr>{"".join(x)}</tr>' for x in vs]) + "\n</tbody>"
    print("<link href=\"./paradigm.css\" rel=\"stylesheet\">")
    print(f'<table class="verb-paradigm">\n{tcontent}\n</table>')
    print()


def layout_participle_summary_paradigm_html(forms, label, labels):
    forms = [f'<td class="para-item">{x}</td>' for x in forms]
    header = [f'<td class="para-header-cell">{labels["number"]}</td>',
             f'<td class="para-header-cell">{labels["case"]}</td>',
             f'<td class="para-header-cell">{labels["masc"]}</td>',
             f'<td class="para-header-cell">{labels["fem"]}</td>',
             f'<td class="para-header-cell">{labels["neut"]}</td>']
    cases =  [f'<td class="para-row-label">{labels["nom"]}</td>',
               f'<td class="para-row-label">{labels["gen"]}</td>'] * 2
    row1 = forms[0:3]
    row2 = forms[3:]
    row1.insert(0, f'<td class="para-row-label">{labels["nom"]}</td>')
    row1.insert(0, f'<td class="para-row-label" valign="top" rowspan="2">{labels["SG"]}</td>')
    row2.insert(0, f'<td class="para-row-label">{labels["gen"]}</td>')
    rows = [row1, row2]
    tcontent = f'<thead><tr class="para-header-row">{"".join(header)}</tr></thead>'
    tcontent += "<tbody>\n" + "\n".join([f'<tr>{"".join(x)}</tr>' for x in rows]) + "\n</tbody>"
    print("<link href=\"./paradigm.css\" rel=\"stylesheet\">")
    print(f'<table class="verb-paradigm">\n{tcontent}\n</table>')
    print()


def layout_merged_verb_paradigm_html(verbs, TVMs, labels):
    verbs = [[f'<td class="para-item">{y}</td>' for y in xs] for xs in verbs]
    row_labels = [f'<td class="para-row-label">{labels[x]}</td>' for x in ['1st', '2nd', '3rd']] * 2
    verbs.insert(0,row_labels)
    header = [f'<td class="para-header-cell">{labels[x]}</td>' if x in labels else f'<td class="para-header-cell">{labels["unknown"]}</td>' for x in TVMs ]
    header.insert(0, f'<td class="para-header-cell">{labels["person"]}</td>')
    header.insert(0, f'<td class="para-header-cell">{labels["number"]}</td>')
    r_verbs = rotate_lists(verbs)
    r_verbs[0].insert(0, f'<td class="para-row-label" rowspan="3" valign="top">{labels["SG"]}</td>')
    r_verbs[3].insert(0, f'<td class="para-row-label" rowspan="3" valign="top">{labels["PL"]}</td>')
    tcontent = f'<thead><tr class="para-header-row">{"".join(header)}</tr></thead>'
    tcontent += "<tbody>\n" + "\n".join([f'<tr>{"".join(x)}</tr>' for x in r_verbs]) + "\n</tbody>"
    print("<link href=\"./paradigm.css\" rel=\"stylesheet\">")
    print(f'<table class="verb-paradigm">\n{tcontent}\n</table>')
    print()


def layout_non_merged_verb_paradigm_html(verbs, tvm, labels):
    row_labels = [f'<td class="para-row-label">{labels[x]}</td>' for x in ['1st', '2nd', '3rd']] * 2
    v = [f'<td class="para-item">{y}</td>' for y in verbs]
    header = [f'<td class="para-header-cell">{labels["number"]}</td>',
             f'<td class="para-header-cell">{labels["person"]}</td>',
             f'<td class="para-header-cell">{labels[tvm]}</td>'if tvm in labels else f'<td class="para-header-cell">{labels["unknown"]}</td>']
    r_verbs = rotate_lists([row_labels, v])
    r_verbs[0].insert(0, f'<td class="para-row-label" rowspan="3" valign="top">{labels["SG"]}</td>')
    r_verbs[3].insert(0, f'<td class="para-row-label" rowspan="3" valign="top">{labels["PL"]}</td>')
    tcontent = f'<thead><tr class="para-header-row">{"".join(header)}</tr></thead>'
    tcontent += "<tbody>\n" + "\n".join([f'<tr>{"".join(x)}</tr>' for x in r_verbs]) + "\n</tbody>"
    print("<link href=\"./paradigm.css\" rel=\"stylesheet\">")
    print(f'<table class="verb-paradigm">\n{tcontent}\n</table>')
    print()


def conjugate_html(lemma, *TVMs, tags=None, labels="labels.yaml", lang="el", merge_paradigms=True):
    labels = load_labels(labels, lang)
    forms = inflexion.conjugate_core(lemma, *TVMs, tags=tags)
    # participles can't be merged with other verb paradigms
    verbs = [(fs[0], list(fs[1].values())) for fs in forms if fs[0][2] in "IOS"]
    imps = [(fs[0], list(fs[1].values())) for fs in forms if fs[0][2] == "D"]
    infs = [(fs[0], list(fs[1].values())) for fs in forms if fs[0][2] == "N"]
    parts = [(fs[0], list(fs[1].values())) for fs in forms if fs[0][2] == "P"]
    if verbs:
        if merge_paradigms:
            tvms = [x[0] for x in verbs]
            verbs = [x[1] for x in verbs]
            layout_merged_verb_paradigm_html(verbs, tvms, labels)
        else:
            for label, v in verbs:
                layout_non_merged_verb_paradigm_html(v, label, labels)
    if imps:
        if merge_paradigms:
            tvms = [x[0] for x in imps]
            imps = [x[1] for x in imps]
            layout_merged_imp_paradigm_html(imps, tvms, labels)
        else:
            for label, v in imps:
                layout_non_merged_imp_paradigm_html(v, label, labels)
    if infs:
        if merge_paradigms:
            layout_merged_inf_paradigm_html(infs, labels)
        else:
            for label, v in infs:
                layout_non_merged_inf_paradigm_html(v, label, labels)
    if parts:
        for label, v in parts:
            layout_participle_summary_paradigm_html(v, label, labels)


def layout_nouny_paradigm_md(forms, labels):
    forms = [[f" {y} " for y in x] for x in forms]
    header = [f' {labels["number"]} ',
             f' {labels["case"]} ',
             f' {labels["masc"]} ',
             f' {labels["fem"]} ',
             f' {labels["neut"]} ']
    cases =  [f' {labels["nom"]} ',
               f' {labels["gen"]} ',
               f' {labels["dat"]} ',
               f' {labels["acc"]} ',
               f' {labels["voc"]} '] * 2
    forms.insert(0, cases)
    numbers = [f' {labels["SG"]} ', ' ', ' ',' ',' ', f' {labels["PL"]} ' , ' ' , ' ', ' ', ' ']
    forms.insert(0, numbers)
    r_forms = rotate_lists(forms)
    tcontent = f'| {"|".join(header)} |\n'
    tcontent += "|:----|:----|:----|:----|:----|\n"
    tcontent += "\n".join([f'|{"|".join(x)}|' for x in r_forms])
    print(tcontent)
    print()


def decline_md(lemma, TVM, tags=None, labels="labels.yaml", lang="el"):
    labels = load_labels(labels, lang)
    forms = [list(x.values()) for x in inflexion.decline_core(lemma, TVM, tags=tags)]
    layout_nouny_paradigm_md(forms, labels)


def layout_nouny_paradigm_html(forms, labels):
    forms = [[f'<td class="para-item">{y}</td>' for y in x] for x in forms]
    header = [f'<td class="para-header-cell">{labels["number"]}</td>',
             f'<td class="para-header-cell">{labels["case"]}</td>',
             f'<td class="para-header-cell">{labels["masc"]}</td>',
             f'<td class="para-header-cell">{labels["fem"]}</td>',
             f'<td class="para-header-cell">{labels["neut"]}</td>']
    cases =  [f'<td class="para-row-label">{labels["nom"]}</td>',
               f'<td class="para-row-label">{labels["gen"]}</td>',
               f'<td class="para-row-label">{labels["dat"]}</td>',
               f'<td class="para-row-label">{labels["acc"]}</td>',
               f'<td class="para-row-label">{labels["voc"]}</td>'] * 2
    forms.insert(0, cases)
    r_forms = rotate_lists(forms)
    r_forms[0].insert(0, f'<td class="para-row-label" rowspan="5" valign="top">{labels["SG"]}</td>')
    r_forms[5].insert(0, f'<td class="para-row-label" rowspan="5" valign="top">{labels["PL"]}</td>')
    tcontent = f'<thead><tr class="para-header-row">{"".join(header)}</tr></thead>'
    tcontent += "<tbody>\n" + "\n".join([f'<tr>{"".join(x)}</tr>' for x in r_forms]) + "\n</tbody>"
    print("<link href=\"./paradigm.css\" rel=\"stylesheet\">")
    print(f'<table class="verb-paradigm">\n{tcontent}\n</table>')
    print()


def decline_html(lemma, TVM, tags=None, labels="labels.yaml", lang="el"):
    labels = load_labels(labels, lang)
    forms = [list(x.values()) for x in inflexion.decline_core(lemma, TVM, tags=tags)]
    layout_nouny_paradigm_html(forms, labels)
