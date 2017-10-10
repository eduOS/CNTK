#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division

# from cntk import constants
from cntk.standardizer import Standardizer
from cntk.cleanser import Cleanser
from cntk.qa.baselines import Baselines
import re
from cntk.constants import keywords
from cntk.tokenizer import JiebaTokenizer
# from cntk.utils import debug

__all__ = ["Processor"]


class Processor(object):
    def __init__(self, sentence=None):
        self._standardizer = Standardizer()
        self._baselines = Baselines()
        self._cleanser = Cleanser()
        self._sentence = sentence
        self._tokenizer = JiebaTokenizer()
        self._regex = None

    def set_sentence(self, sentence):
        self._sentence = sentence
        return self

    def set_myregex(self, regex=None):
        """
        input:
            the regex for the filter
        """
        regex = regex if regex else '|'.join(
            [keywords.NUMBER_KWS,
             keywords.COARSE_KWS,
             ])
        self._regex = re.compile(regex)

    def preprocess(self):
        self._sentence = self._standardizer.set_sentence(
            self._sentence).standardize().sentence
        self._sentence = self._cleanser.set_sentence(
            self._sentence).delete_whitespace().sentence
        # self._sentence = self.my_filter()._sentence
        return self

    def clean(self):
        """
        inner delete
        """
        self._sentence = self._cleanser.set_sentence(
            self._sentence).clean().sentence
        # print('after cleaning '+self._sentence)
        return self

    def standardize(self):
        """
        modify
        """
        self._sentence = self._standardizer.set_sentence(
            self._sentence).standardize('all').sentence
        return self

    @property
    def sentence(self):
        return self._sentence

    def my_filter(self):
        """
        delete
        """
        if self._regex is None:
            self.set_myregex()
        baseline = self._baselines.set_sentence(
            self._sentence
        ).meet_length(
            2, 100
        ).meet_chinese(chinese=2/3).has_dealbreaker(self._regex)
        self._sentence = baseline.sentence
        self._reason = baseline.reason
        # print('after filtering '+unicode(self._sentence))
        return self

    def __call__(self, sentence, tokenize=False, std=False):
        if sentence:
            self.set_sentence(sentence).preprocess().clean()
            if std:
                self.standardize()
            self.my_filter()
            if tokenize:
                words = self._tokenizer.sentence2words(self._sentence)
                if words:
                    self._sentence = ' '.join(words)
            return self.sentence, self._reason
        elif self.sentence:
            self.set_sentence(sentence).preprocess().clean()
            if std:
                self.standardize()
            self.my_filter()
            return self.sentence, self._reason
