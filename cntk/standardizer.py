#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
import unicodedata
import os
import re

from cntk.constants.punctuation import Punctuation
from cntk.constants.mathre import Math2ZH
from cntk.constants.units import Unit2ZH
from cntk.constants.timere import Time2ZH
from cntk.utils import not_none, safely_sub, further_sub, BaseProcessor
from cntk.constants.offals import Offals

__all__ = ['Standardizer', 'Converter']


class Converter(object):
    """
    convert tranditional Chinese to Simplified Chinese
    """
    def __init__(self):
        if os.system("opencc --version") != 0:
            raise Exception("Opencc not installed")

    def convert(self, fin, fout):
        """
        convert tranditional chinese to simplified chinese
        """
        cmd = "opencc -i %s -o %s -c zht2zhs.ini"
        os.system(cmd % (fin, fout))
        os.system("mv %s %s" % (fout, fin))


class Standardizer(BaseProcessor):
    def __init__(self, sentence=0):
        super(Standardizer, self).__init__(sentence)

    @not_none
    def to_lowercase(self):
        self._sentence = self._sentence.lower()
        return self

    @not_none
    def fwidth2hwidth(self):
        self._sentence = unicodedata.normalize('NFKC', self._sentence)
        return self

    @not_none
    def zh_punc2en_punc(self, reverse=False):
        """
        replace the English punctuations in sentence to Chinese ones
        """
        punfrom = Punctuation.EN_PUNC if reverse else Punctuation.ZH_PUNC
        punto = Punctuation.ZH_PUNC if reverse else Punctuation.EN_PUNC
        punfrom = punfrom.split('|')
        punto = punto.split('|')

        dic = dict(zip(punfrom, punto))
        for punc in punfrom:
            if punc in self._sentence:
                self._sentence = self._sentence.replace(punc, dic[punc])
        return self

    @safely_sub
    def math_frac(self):
        """
        transform the fraction of the form 1/2 to the form like 2分之1
        """
        return Math2ZH.frac()

    @safely_sub
    def math_int(self):
        """
        delete useless point zeros of ints
        """
        return Math2ZH.myint()

    @safely_sub
    def unit_latnlon(self):
        '''
        transform angle to 度， 分， 秒
        '''
        return Unit2ZH.latnlon()

    @safely_sub
    def unit_per(self):
        return Unit2ZH.per()

    @safely_sub
    def unit_percent(self):
        return Unit2ZH.percent()

    @safely_sub
    def unit_temp(self):
        """
        temperature
        """
        return Unit2ZH.temp()

    @further_sub(Unit2ZH.unit_en2zh3())
    @safely_sub
    def unit_range(self):
        return Unit2ZH.myrange()

    @safely_sub
    def unit_date(self):
        return Unit2ZH.date()

    @safely_sub
    def unit_time(self):
        return Unit2ZH.time()

    @safely_sub
    def unit_en2zh0(self):
        """
        for units which are between chinese characters
        """
        return Unit2ZH.unit_en2zh0()

    @safely_sub
    def brand_en2zh(self):
        pass

    @safely_sub
    def unit_en2zh1(self):
        """
        for units which are certain
        """
        return Unit2ZH.unit_en2zh1()

    @safely_sub
    def unit_en2zh2(self):
        # units not in range
        return Unit2ZH.unit_en2zh2()

    @safely_sub
    def math_percent(self):
        # units not in range
        return Math2ZH.percent()

    @safely_sub
    def time_zero(self):
        return Time2ZH.zero()

    @safely_sub
    def zero_one(self):
        return Math2ZH.zeroorone()

    @safely_sub
    def digits(self, repl="*"):
        """
        replace non (repetitive) chinese characters with repl
        """
        return Offals.digits(repl)

    @not_none
    def cut_or_add_punc(self):
        """
        delete " with sentence dilimiters in it
        """
        new_sentence = ""
        if not re.search('"', self._sentence):
            return self
        for n, w in enumerate(self._sentence.split('"')):
            if n % 2 and re.search('[,.;!]', w):
                new_sentence += '"' + w + '"'
            else:
                new_sentence += w
        self._sentence = new_sentence
        return self

    @not_none
    def standardize(self, mode="basic"):
        """
        mode can be basic and all
        if all:
            transfer all units and math characters
        """
        # if mode is basic then change full width characters to half width ones,
        # and change chinese punctuations to english ones
        if mode == "basic":
            self.to_lowercase().zh_punc2en_punc().fwidth2hwidth(
            ).unit_percent().unit_range().cut_or_add_punc().unit_time()
        elif mode == "all":
            """
            the default sub order
            """
            self.to_lowercase().zh_punc2en_punc().fwidth2hwidth(
            ).math_int().unit_date().math_frac().unit_per(
            ).unit_percent().unit_range().unit_en2zh0().unit_en2zh1(
            ).unit_en2zh2().unit_temp().unit_latnlon().unit_time(
            ).zero_one().time_zero().math_percent()
        return self
