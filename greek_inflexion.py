from collections import defaultdict
import re

from inflexion import Inflexion

from accent import calculate_accent, strip_accents, debreath, rebreath
from fileformat import load_stemming, load_lexicon


class GreekInflexion:

    def __init__(self, stemming_file, lexicon_file):

        self.ruleset = load_stemming(stemming_file)

        self.lexicon, self.form_override, self.accent_override = load_lexicon(
            lexicon_file, pre_processor=debreath)

        self.inflexion = Inflexion()
        self.inflexion.add_lexicon(self.lexicon)
        self.inflexion.add_stemming_rule_set(self.ruleset)

    def find_stems(self, lemma, key, tags=None):
        return self.lexicon.find_stems(lemma, key, tags)

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
                accent_form = calculate_accent(
                    orig_form, key, lemma, detail["stem"],
                    self.inflexion, self.accent_override)
                detail.update({"original_form": orig_form})
                generated[accent_form].append(detail)
        return generated

    def possible_stems(self, form, key_regex=None):
        for key, stem in self.ruleset.possible_stems(debreath(form)):
            if key_regex is None or re.match(key_regex, key):
                yield key, rebreath(strip_accents(stem))

    def parse(self, form):
        return self.inflexion.parse(
            debreath(form), stem_post_processor=strip_accents)
