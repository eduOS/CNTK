#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
import re

from cntk.constants import offals
from cntk.utils import not_none, BaseProcessor
from cntk.constants.punctuation import Punctuation
from cntk.utils import safely_del
import html2text

__all__ = ['Cleanser']

translate_table = dict((ord(char), ' ') for char in Punctuation.ALL_PUNC)


class Cleanser(BaseProcessor):
    # TODO: a classmethod to initialize this class
    def __init__(self, sentence=0):
        super(Cleanser, self).__init__(sentence)
        self.h = None

    # the function claining: http://qr.ae/TAiBAr

    def clean_html(self, html):
        if not self.h:
            self.h = html2text.HTML2Text()
            self.h.ignore_links = True
            self.h.ignore_tables = True
            self.h.ignore_images = True
            self.h.blockquote = True
            self.h.drop_white_space = True
            self.h.ignore_emphasis = True
            self.h.body_width = 0
            # the newline problem: https://stackoverflow.com/a/12839212/3552975
        return self.h.handle(html)

    @not_none
    def delete_whitespace(self):
        self._sentence = self._sentence.strip()
        self._sentence = re.sub('(?<!\w)\s(?!\w)', '', self._sentence)
        # print(self._sentence)
        return self

    @not_none
    def delete_offals(self):
        # self._sentence = re.sub(offals.LINK, '', self._sentence)
        # self._sentence = re.sub(offals.BULLET, '', self._sentence)
        # self._sentence = re.sub(offals.ADDITION, '', self._sentence)
        # self._sentence = re.sub(offals.PARENOTE, '', self._sentence)
        # self._sentence = re.sub(offals.FORWARD, '', self._sentence)
        # self._sentence = re.sub(offals.CONJUNCTION, '', self._sentence)
        return self.del_links(
        ).del_bullet().del_forward().del_addition().del_parenote()

    @safely_del(offals.FORWARD)
    def del_forward(self, *args):
        return

    @safely_del(offals.ADDITION)
    def del_addition(self, *args):
        return

    # TODO
    # @not_none
    # @staticmethod
    # def del_all_punc(self, sentence=0):
    #     # https://stackoverflow.com/a/1324114/3552975
    #     if sentence == 0:
    #         self._sentence = self._sentence.translate(translate_talbe)
    #     else:
    #         sentence = sentence.translate(translate_talbe)
    #         return sentence

    #     return self

    @not_none
    def del_all_punc(self):
        # https://stackoverflow.com/a/1324114/3552975
        self._sentence = self._sentence.translate(translate_table)
        return self

    @safely_del(offals.PARENOTE)
    def del_parenote(self, *args):
        return

    @safely_del(offals.BULLET)
    def del_bullet(self, *args):
        return

    @safely_del(offals.LINK)
    def del_links(self, *args):
        return

    # @not_none
    # def strip_punc(self):
    #     """
    #     offals should be first deleted
    #     all chinese punc should be transfered to english ones
    #     """
    #     self._sentence = self._sentence.strip(Punctuation.ALL.replace('"', ''))
    #     # the self._sentence should not start with punctuations and ends with
    #     # non stop punc
    #     # nonstart = "".join(
    #     #     list(set(constants.punc) - set(constants.sentencestart)))
    #     # nonstopend = "".join(
    #     #     list(set(constants.punc) - set(constants.nonstopend)))
    #     # delete all non_sentence end and stops(for delete all duplicates)
    #     # self._sentence = self._sentence.lstrip(nonstart).rstrip(nonstopend)
    #     self._sentence = re.sub(Punctuation.USELESS, "", self._sentence)
    #     # print('after sub: '+self._sentence)
    #     return self

    def simply_clean(self):
        """
        clean public articles such as news and the alike published by
        offical agents
        """
        return self.del_links(
        ).del_parenote().del_bullet().del_addition()._sentence

    def clean(self):
        return self.delete_offals().strip_punc()
