#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
import unicodedata
import os

from cntk.constants.punctuation import Punctuation
from cntk.utils import safely_del
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
    def to_lowercase(self, verbose=False):
        self._sentence = self._sentence.lower()
        return self

    @not_none
    def fwidth2hwidth(self, verbose=False):
        self._sentence = unicodedata.normalize('NFKC', self._sentence)
        return self

    @not_none
    def zh_punc2en_punc(self, reverse=False, verbose=False):
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
    def math_frac(self, verbose=False):
        """
        transform the fraction of the form 1/2 to the form like 2分之1
        """
        return Math2ZH.frac()

    @safely_sub
    def math_int(self, verbose=False):
        """
        delete useless point zeros of ints
        """
        return Math2ZH.myint()

    @safely_sub
    def unit_latnlon(self, verbose=False):
        '''
        transform angle to 度， 分， 秒
        '''
        return Unit2ZH.latnlon()

    @safely_sub
    def unit_per(self, verbose=False):
        return Unit2ZH.per()

    @safely_sub
    def unit_percent(self, verbose=False):
        return Unit2ZH.percent()

    @safely_sub
    def unit_temp(self, verbose=False):
        """
        temperature
        """
        return Unit2ZH.temp()

    @further_sub(Unit2ZH.unit_en2zh3())
    @safely_sub
    def unit_range(self, verbose=False):
        return Unit2ZH.myrange()

    @safely_sub
    def unit_date(self, verbose=False):
        return Unit2ZH.date()

    @safely_sub
    def unit_time(self, verbose=False):
        return Unit2ZH.time()

    @safely_sub
    def unit_en2zh0(self, verbose=False):
        """
        for units which are between chinese characters
        """
        return Unit2ZH.unit_en2zh0()

    @safely_sub
    def brand_en2zh(self, verbose=False):
        pass

    @safely_del(Offals.periods())
    def initialism(self, verbose=False):
        return

    @safely_sub
    def unit_en2zh1(self, verbose=False):
        """
        for units which are certain
        """
        return Unit2ZH.unit_en2zh1()

    @safely_sub
    def unit_en2zh2(self, verbose=False):
        # units not in range
        return Unit2ZH.unit_en2zh2()

    @safely_sub
    def math_percent(self, verbose=False):
        # units not in range
        return Math2ZH.percent()

    @safely_sub
    def time_zero(self, verbose=False):
        return Time2ZH.zero()

    @safely_sub
    def zero_one(self, verbose=False):
        return Math2ZH.zeroorone()

    @safely_sub
    def digits(self, repl="*", verbose=False):
        """
        replace non (repetitive) chinese characters with repl
        """
        return Offals.digits(repl)

    @safely_sub
    def order_number(self, repl=",", verbose=False):
        return Offals.order_number(repl)

    @not_none
    def standardize(self, mode="basic", verbose=False):
        """
        mode can be basic and all
        if all:
            transfer all units and math characters
        """
        # if mode is basic then change full width characters to half width ones,
        # and change chinese punctuations to english ones
        if mode == "basic":
            self.to_lowercase().zh_punc2en_punc().fwidth2hwidth(
            ).unit_percent().unit_range().unit_time()
        elif mode == "all":
            """
            the default sub order
            """
            self.to_lowercase().zh_punc2en_punc().fwidth2hwidth(
            ).initialism().math_int().unit_date().math_frac().unit_per(
            ).unit_percent().unit_range().unit_en2zh0().unit_en2zh1(
            ).unit_en2zh2().unit_temp().unit_latnlon().unit_time(
            ).zero_one().time_zero().math_percent()
        return self
