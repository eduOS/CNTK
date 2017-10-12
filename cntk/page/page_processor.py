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
import warnings
from cntk.constants import keywords
from cntk.tokenizer import JiebaTokenizer
# from cntk.utils import debug

__all__ = ["Processor"]


class Processor(object):
    def __init__(self, sentence=None):
        self._standardizer = Standardizer()
        self._baselines = Baselines()
        self._cleanser = Cleanser()
        self._sentences = []
        self._tokenizer = JiebaTokenizer()
        self._regex = None

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

    def set_page(self, page, is_html=True):
        if is_html:
            page = self._cleanser.clean_html(page)
        self._page = page
        return self

    def preprocess(self, sentence):
        sentence = self._standardizer.set_sentence(
            sentence).standardize().sentence
        sentence = self._cleanser.set_sentence(
            sentence).delete_whitespace().sentence
        return sentence

    def clean(self, sentence):
        """
        inner delete
        """
        return self._cleanser.set_sentence(sentence).clean().sentence

    @property
    def sentences(self):
        return self._sentences

    def filter_out(self, sentence, min_len, max_len, chinese_rate):
        """
        delete
        """
        if not self._regex:
            warnings.warn("Only number_kws and coarse_kws are set.")
            self.set_myregex()
        sentence = self._baselines.set_sentence(
            sentence
        ).meet_length(
            min_len, max_len
        ).meet_chinese(
            chinese=chinese_rate).has_dealbreaker(self._regex).sentence
        # print('after filtering '+unicode(self._sentence))
        return sentence

    def standardize(self, sentence):
        """
        units and others
        """
        sentence = self._standardizer.set_sentence(
            sentence).standardize('all').sentence
        return sentence

    def select_sentences(
        self, page, is_html=True, min_len=2,
        max_len=100, std=False, chinese_rate=2/3,
    ):
        try:
            sentences = [
                self.preprocess(st) for st in self._tokenizer.text2sentences(
                    self.set_page(page, is_html)._page)
            ]
            sentences = [
                st for st in sentences
                if self.filter_out(st, min_len, max_len, chinese_rate)]
            if std:
                sentences = [self.standardize(st) for st in sentences]
            self._sentences = sentences = [self.clean(st) for st in sentences]
        except:
            warnings.warn("No sentences returned when selecting sentences.")
            return None

        return sentences

    def __call__(
        self, page, is_html=True, min_len=2,
        max_len=100, std=False, chinese_rate=2/3,
    ):
        return self.select_sentences(
            page, is_html, min_len, max_len, std, chinese_rate)
