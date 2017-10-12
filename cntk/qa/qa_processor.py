#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division

# from cntk import constants
from cntk.standardizer import Standardizer
from cntk.cleanser import Cleanser
from cntk.qa.baselines import Baselines
import jieba
import collections
# from cntk import constants
import re
from cntk.constants import keywords
# from cntk.utils import debug

__all__ = ['QuestionProcessor', 'AnswerProcessor']


class Processor(object):
    def __init__(self, sentence=None):
        self._standardizer = Standardizer()
        self._baselines = Baselines()
        self._cleanser = Cleanser()
        self._sentence = sentence
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

    def my_filter(self, min_len, max_len, chinese_rate):
        """
        delete
        """
        if self._regex is None:
            self.set_myregex()
        baseline = self._baselines.set_sentence(
            self._sentence
        ).meet_length(
            min_len, max_len
        ).meet_chinese(chinese_rate).has_dealbreaker(self._regex)
        self._sentence = baseline.sentence
        self._reason = baseline.reason
        # print('after filtering '+unicode(self._sentence))
        return self


class AnswerProcessor(Processor):
    def __init__(self, min_len=6, max_len=30, sentence=None):
        super(AnswerProcessor, self).__init__(sentence)
        self._min_len = min_len
        self._max_len = max_len

    @classmethod
    def out_lowfreq_words(fin, fout, wfrq=2):
        """
        filter out lines with answers containing low frequency words
        inputs:
            fin: the file which should be processed
            fout: where the processed result to write
            wfrq: the word frequency threshold
        outputs:
            only lines with answer containing words that all occur more than
            wfrq times
        """

        counter = collections.Counter()
        # this can be optimized: not all items should be recorded
        with open(fin, "r", 'utf-8') as f:
            lines = f.readlines()
            for line in lines:
                answer = line.split("@@")[-1].strip()
                if answer.strip() != "":
                    unigram = jieba.cut(answer)
                    counter.update(unigram)

        # least = [i for i in counter if counter.get(i) > no]

        fout = open(fout, "w", 'utf-8')
        # fout.write(str(counter))

        with open(fin, "r", 'utf-8') as f:
            for line in f:
                answer = line.split("@@")[-1].strip()
                # items = jieba.cut(answer, HMM=False)
                items = jieba.cut(answer, HMM=True)
                # set the HMM as False to avoid generating new words
                if min(map(counter.get, items)) >= wfrq:
                    fout.write(line)
        fout.close()

    @property
    def answer(self):
        return self._sentence

    def __call__(self, answer, std=False):
        """
        input:
            std: if true unites will be standardized
        return:
            answer(or question) and reason, one for the processed text and the
            other for why the question or answer has been deleted if the reason
            is not ""
        """
        self.set_sentence(answer).preprocess().clean()
        if std:
            self.standardize()
        self.my_filter(self._min_len, self._max_len, 2/3)
        return self.answer, self._reason
        # print(self.answer)


class QuestionProcessor(Processor):
    def __init__(self, min_len=6, max_len=30, question=None):
        super(QuestionProcessor, self).__init__(question)
        self._max_len = max_len
        self._min_len = min_len

    def shorten(self):
        if not self._sentence:
            return self

        elif len(self._sentence) > self._max_len:
            new_question = self._sentence
            questions = re.split("[?。!]", self._sentence)
            if len(questions) > 1:
                for i in range(len(questions)):
                    new_question = questions[:len(questions)-i]
                    new_question = "?".join(new_question)
                    if len(new_question) < self._max_len:
                        self._sentence = new_question
                        if len(self._sentence) < self._min_len:
                            self._sentence = None
                        return self
            else:
                self._sentence = None

            return self

        elif len(self._sentence) < self._min_len:
            self._sentence = None

        return self

    @property
    def question(self):
        return self._sentence

    def __call__(self,
                 question, std=False, chinese_rate=2/3):
        self.set_sentence(question).preprocess().clean()
        if std:
            self.standardize()
        self.my_filter(self._min_len, self._max_len, chinese_rate)
        return self.question, self._reason
