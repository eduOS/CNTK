#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
import re

from cntk.constants import offals
from termcolor import colored
from cntk.utils import not_none, BaseProcessor
from cntk.constants.punctuation import Punctuation
from cntk.utils import safely_del
from cntk.utils import regex_compile
import html2text

__all__ = ['Cleanser']


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
        """
        delete unnecessary white space between chinese but keep those necessary
        between English words
        """
        self._sentence = self._sentence.strip()
        self._sentence = re.sub(regex_compile('(?<!(\w|\.))\s(?!(\w|\.))'), '', self._sentence)
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

    @not_none
    def del_all_punc(self, except_=u"", repl=u" "):
        # something wrong here
        # u"；()、" in the except will be deleted alwasy"
        # https://stackoverflow.com/a/1324114/3552975
        all_punc = unicode(Punctuation.ALL_PUNC) # NOQA
        repl = unicode(repl) # NOQA
        if not repl:
            repl = None
        all_punc = set(all_punc) - set(except_)
        if " " in all_punc:
            print(colored(
                "Warning: space will be deleted(in del_all_punc func).. if this is unexpected delete the space from punc", 'red'))
        self._sentence = re.sub(r"\.(?=\d)", "dooooooog", self._sentence)
        translate_table = dict((ord(char), repl) for char in all_punc)
        self._sentence = self._sentence.translate(translate_table)
        self._sentence = re.sub("dooooooog(?=\d)", ".", self._sentence)
        return self

    @not_none
    def del_punc(self, puncs, repl=" "):
        """
        replace all punc in puncs with repl
        """
        self._sentence = re.sub("\.(?=\d)", "dooooooog", self._sentence)
        translate_table = dict((ord(p), repl) for p in puncs)
        if "" in translate_table:
            print(colored(
                "Warning: space will be deleted(in del_punc func).. if this is unexpected delete the space from punc", 'red'))
        self._sentence = self._sentence.translate(translate_table)
        self._sentence = re.sub("dooooooog(?=\d)", ".", self._sentence)
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

    @not_none
    def unnecessary_quot(self):
        """
        unnecessary quotations mean quotations with sentence dilimiters in it
        """
        new_sentence = ""
        if not re.search('"', self._sentence):
            return self
        for n, w in enumerate(self._sentence.split('"')):
            if n % 2 and re.search(Punctuation.SENTENCE_DELIMITERS, w):
                new_sentence += '"' + w + '"'
            else:
                new_sentence += w
        self._sentence = new_sentence
        return self

    @safely_del
    def repeating_delimiters(self):
        pass

    @safely_del(Punctuation.USELESS)
    def delete_useless(self, *args):
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
        return self.del_links().del_parenote().del_bullet().del_addition().sentence

    def clean(self):
        return self.delete_offals().del_all_punc()
