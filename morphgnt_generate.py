#!/usr/bin/env python3

from pysblgnt import morphgnt_rows

from accent import strip_length  # , rebreath
from greek_inflexion import GreekInflexion
from morphgnt_utils import bcv_tuple, convert_parse

ginflexion = GreekInflexion("stemming.yaml", "morphgnt_johannine_lexicon.yaml")

debug = False


incorrect_count = 0
total_count = 0

for book_num in [4, 23, 24, 25]:
    for row in morphgnt_rows(book_num):
        b, c, v = bcv_tuple(row["bcv"])
        if row["ccat-pos"] == "V-":
            total_count += 1

            lemma = row["lemma"]
            key = convert_parse(row["ccat-parse"])
            form = row["norm"]

            tags = set([
                "final-nu-aai.3s",
                "oida-yai3p-variant",
                "no-final-nu-yai.3s",
                "late-pluperfect-singulars",
                "HGrk",
            ])

            c = form.count("/") + 1
            stem = ginflexion.find_stems(lemma, key, tags)
            generated = ginflexion.generate(lemma, key, tags)

            if stem:
                stem_guess = None
            else:
                stem_guess = [
                    stem for key, stem in
                    ginflexion.possible_stems(form, "^" + key + "$")]

            # if [strip_length(w) for w in sorted(generated)] == \
            #         [strip_length(w) for w in sorted(form.split("/"))]:
            #     correct = "✓"
            # else:
            #     correct = "✕"
            #     incorrect_count += 1

            if strip_length(form) in [
                    strip_length(w) for w in sorted(generated)]:
                correct = "✓"
            else:
                correct = "✕"
                incorrect_count += 1

            if debug or correct == "✕":
                print("-")
                print("    lemma: {}".format(lemma))
                print("    key: {}".format(key))
                print("    form: {}".format(form))
                if stem:
                    if len(stem) == 1:
                        print("    stem: {}".format(list(stem)[0]))
                    else:
                        print("    stem: {}".format(list(stem)))
                if stem_guess:
                    print("    stem_guess: {}".format(stem_guess))
                print("    correct: \"[{}/{}{}]\"".format(
                    len(generated), c, correct))
                print("    generated:")
                for generated_form, details in generated.items():
                    print("      -")
                    print("        form: {}".format(generated_form))
                    print("        details:")
                    for detail in details:
                        print("          -")
                        if "stem" in detail:
                            print("            stem: {}".format(detail["stem"]))
                        if "stemming" in detail:
                            print("            stemming:")
                            print("                base: {}".format(detail["stemming"]["base"]))
                            print("                ending: {}".format(detail["stemming"]["ending"]))
                            print("                rule: \"{0.a}|{0.b}>{0.c}<{0.d}|{0.e}\"".format(detail["stemming"]["rule"]))
                            print("                used_default: {}".format(detail["stemming"]["used_default"]))
                        if "original_form" in detail:
                            print("            original_form: {}".format(detail["original_form"]))
                        if "override" in detail:
                            print("            override: {}".format(detail["override"]))

print("{}/{} incorrect".format(incorrect_count, total_count))

            # c = form.count("/") + 1
            # stem = ginflexion.find_stems(lemma, key, tags)
            # generated = ginflexion.generate(lemma, key, tags)
            #
            # for generated_form, details in generated.items():
            #     if form == generated_form:
            #         for i, detail in enumerate(details):
            #
            #             print("{:12s}".format(lemma), end="\t")
            #             print("{:8s}".format(key), end="\t")
            #             print("{:16s}".format(form), end="\t")
            #             print("{:24s}".format("/".join(stem)), end="\t")
            #
            #             print("{:2d}".format(i), end="\t")
            #             print("{:24s}".format(rebreath(detail.get("stem", "-"))), end="\t")
            #
            #             if "stemming" in detail:
            #                 print("{:12s}".format(rebreath(detail["stemming"]["base"]) or "-"), end="\t")
            #                 print("{:8s}".format(detail["stemming"]["ending"] or "-"), end="\t")
            #                 print("{0.a}|{0.b}>{0.c}<{0.d}|{0.e}".format(detail["stemming"]["rule"]))
            #             else:
            #                 print()
