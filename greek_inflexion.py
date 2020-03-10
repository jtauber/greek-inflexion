from collections import defaultdict
import re

from inflexion import Inflexion
from inflexion.lexicon import Lexicon

from accent import calculate_accent, strip_accents, debreath, rebreath
from fileformat import load_stemming, load_lexicon


class GreekInflexion:

    def __init__(self, stemming_file, lexicon_file=None, strip_length=False):

        self.ruleset = load_stemming(stemming_file, strip_length)

        if lexicon_file:
            (
                self.lexicon, self.form_override, self.accent_override,
                self.segmented_lemmas
            ) = load_lexicon(lexicon_file, pre_processor=debreath)
        else:
            self.lexicon = Lexicon()
            self.form_override = {}
            self.accent_override = defaultdict(list)
            self.segmented_lemmas = {}

        self.inflexion = Inflexion()
        self.inflexion.add_lexicon(self.lexicon)
        self.inflexion.add_stemming_rule_set(self.ruleset)

    def find_stems(self, lemma, key, tags=None):
        return self.lexicon.find_stems(
            lemma, key, tags, stem_post_processor=rebreath)

    def generate(self, lemma, key, tags=None):
        overrides = self.form_override.get((lemma, key))
        if overrides:
            if isinstance(overrides, str):
                overrides = [overrides]
            return {
                override: [{"override": "form"}]
                for override in overrides
            }
        generated = defaultdict(list)
        for orig_form, details in self.inflexion.generate(
                lemma, key, tags).items():
            for detail in details:
                segmented_lemma = self.segmented_lemmas.get(lemma)
                accent_form, accent_notes = calculate_accent(
                    orig_form, key, lemma, segmented_lemma, detail["stem"],
                    self.inflexion, self.accent_override)
                detail.update({"original_form": orig_form})
                detail.update({"accent_notes": accent_notes})
                generated[accent_form].append(detail)
        return generated

    def possible_stems(self, form, key_regex=None):
        for key, stem in self.ruleset.possible_stems(debreath(form)):
            if key_regex is None or re.match(key_regex, key):
                if stem != "h":
                    yield key, rebreath(strip_accents(stem))

    def possible_stems2(self, form, key_regex=None):
        for key, stem in self.ruleset.possible_stems2(debreath(form)):
            if key_regex is None or re.match(key_regex, key):
                yield key, rebreath(strip_accents(stem))

    def parse(self, form):
        return self.inflexion.parse(
            debreath(form), stem_post_processor=strip_accents)

    def conjugate(self, lemma, *TVMs, tags=None):
        print("-")
        print("    lemma: {}".format(lemma))
        if tags:
            print()
            print("    tags:")
            for tag in tags:
                print("      - {}".format(tag))
        for TVM in TVMs:
            print()
            if TVM[2] in "ISO":
                for PN in ["1S", "2S", "3S", "1P", "2P", "3P"]:
                    parse = TVM + "." + PN
                    form = "/".join(
                        self.generate(lemma, parse, tags=tags).keys())
                    if form:
                        print("    {}: {}".format(parse, form))
            elif TVM[2] == "D":
                if "." not in TVM:
                    for PN in ["2S", "3S", "2P", "3P"]:
                        parse = TVM + "." + PN
                        form = "/".join(
                            self.generate(lemma, parse, tags=tags).keys())
                        if form:
                            print("    {}: {}".format(parse, form))
                else:
                    form = "/".join(
                        self.generate(lemma, parse, tags=tags).keys())
                    if form:
                        print("    {}: {}".format(TVM, form))
            elif TVM[2] == "N":
                parse = TVM
                form = "/".join(
                    self.generate(lemma, parse, tags=tags).keys())
                if form:
                    print("    {}: {}".format(parse, form))
            elif TVM[2] == "P":
                if TVM.endswith(".N"):
                    for NG in ["SM", "SF", "SN"]:
                        parse = TVM + NG
                        form = "/".join(
                            self.generate(lemma, parse, tags=tags).keys())
                        if form:
                            print("    {}: {}".format(parse, form))
                else:
                    for CNG in ["NSM", "NSF", "NSN", "GSM", "GSF", "GSN"]:
                        parse = TVM + "." + CNG
                        form = "/".join(
                            self.generate(lemma, parse, tags=tags).keys())
                        if form:
                            print("    {}: {}".format(parse, form))
        print()
        print()

    def conjugate_core(self, lemma, *TVMs, tags=None):
        result = []
        for TVM in TVMs:
            out = {}
            if TVM[2] in "ISO":
                for PN in ["1S", "2S", "3S", "1P", "2P", "3P"]:
                    parse = TVM + "." + PN
                    form = "/".join(
                        self.generate(lemma, parse, tags=tags).keys())
                    if form:
                        out[parse] = form
            elif TVM[2] == "D":
                if "." not in TVM:
                    for PN in ["2S", "3S", "2P", "3P"]:
                        parse = TVM + "." + PN
                        form = "/".join(
                            self.generate(lemma, parse, tags=tags).keys())
                        if form:
                            out[parse] = form
                else:
                    form = "/".join(
                        self.generate(lemma, parse, tags=tags).keys())
                    if form:
                        out[parse] = form
            elif TVM[2] == "N":
                parse = TVM
                form = "/".join(
                    self.generate(lemma, parse, tags=tags).keys())
                if form:
                    out[parse] = form
            elif TVM[2] == "P":
                if TVM.endswith(".N"):
                    for NG in ["SM", "SF", "SN"]:
                        parse = TVM + NG
                        form = "/".join(
                            self.generate(lemma, parse, tags=tags).keys())
                        if form:
                            out[parse] = form
                else:
                    for CNG in ["NSM", "NSF", "NSN", "GSM", "GSF", "GSN"]:
                        parse = TVM + "." + CNG
                        form = "/".join(
                            self.generate(lemma, parse, tags=tags).keys())
                        if form:
                            out[parse] = form
            result.append((TVM, out))
        return result

    def decline_core(self, lemma, TVM, tags=None):
        if TVM[2] != "P":
            raise ValueError
        result = []
        for G in "MFN":
            forms = {}
            for CN in [
                "NS", "GS", "DS", "AS", "VS",
                "NP", "GP", "DP", "AP", "VP"
            ]:
                parse = TVM + "." + CN + G
                form = "/".join(
                    self.generate(lemma, parse, tags=tags).keys())
                if form:
                    forms[parse] = form
            result.append(forms)
        return result

    def decline(self, lemma, TVM, tags=None):

        if TVM[2] != "P":
            raise ValueError

        print("-")

        print("    lemma: {}".format(lemma))

        for G in "MFN":
            print()
            for CN in [
                "NS", "GS", "DS", "AS", "VS",
                "NP", "VP", "GP", "DP", "AP"
            ]:
                parse = TVM + "." + CN + G
                form = "/".join(
                    self.generate(lemma, parse, tags=tags).keys())
                print("    {}: {}".format(parse, form))

        print()
        print()
