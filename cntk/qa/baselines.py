#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
from cntk.hanzi_identifier import (
    has_chinese, has_only_chinese, get_ch_ratio, has_leetspeak, has_non_cjk)
from cntk import constants
from cntk.utils import not_none
import re

__all__ = ['Baselines']


class Baselines(object):
    # the implementation should be improved in dealing with the returned None or
    # False
    def __init__(self):
        self._sentence = None

    def set_sentence(self, sentence):
        self.origin_sentence = self._sentence = sentence
        self._reason = ""
        if sentence is None or sentence.strip() == "":
            self._sentence = None
        return self

    def is_none(self):
        return not bool(self._sentence)

    @property
    def sentence(self):
        return self._sentence

    @not_none
    def meet_length(self, min_len=2, max_len=30):
        sentence_length = len(self._sentence.strip(constants.punc+" \n\t"))
        if sentence_length < min_len or sentence_length > max_len:
            self._reason = "Length out the range of %s - %s" % (
                str(min_len), str(max_len))
            self._sentence = None
        return self

    @not_none
    def meet_chinese(self, chinese=2/3):
        """
        more baselines can be added here
        input:
            chinese: if 0 there can be no any chinese in the sentence
                     if 0 < chinese < 1,
                        the chinese/(nonchinese+chinese) ratio should be
                     if 1 there must be only chinese in the sentence
        """
        if chinese > 0 and not has_chinese(self._sentence):
            self._sentence = None
            self._reason = "No Chinese"
            return self
        elif chinese == 1 and not has_only_chinese(self._sentence):
            self._sentence = None
            self._reason = "NonChinese exists"
            return self
        # elif has_leetspeak(self._sentence) or has_non_cjk(self._sentence):
        #     self._sentence = None
        #     self._reason = "Leetspeak or noncjk characters exist"
        #     return self
        # elif get_ch_ratio(self._sentence) < chinese:
        #     self._sentence = None
        #     self._reason = "Too much nonChinese"
        #     return self
        return self

    @not_none
    def has_continuous_english(self, lw_len=4, up_len=6):
        if re.search(
            "[a-z ]{%s,}" % str(lw_len), self._sentence) or re.search(
                "[A-Z ]{%s,}" % str(up_len), self._sentence):
            self._reason = "Low cases or uppercase out of range(%s, %s)" % (
                str(lw_len), str(up_len))
            self._sentence = None
            return self
        return self

    @not_none
    def has_continuous_numbers(self, num_len=5):
        if re.search("[0-9]{%s,}" % str(num_len), self._sentence):
            self._reason = "Countinuous numbers longer than %s" % str(num_len)
            self._sentence = None
        return self

    @not_none
    def has_dealbreaker(self, regex=None):
        # if the length is longer than a certain number it is a story
        if re.search(regex, self._sentence):
            self._sentence = None
            self._reason = "Keywords hit"
            return self
        return self

    @property
    def reason(self):
        return self._reason
