#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import jieba
import jieba.posseg as posseg
import sys
from . import constants
import re
from cntk.cleanser import Cleanser
from cntk.utils import regex_compile

__all__ = ['JiebaTokenizer']


class Tokenizer(object):
    def __init__(self):
        self._sentencedelimiters = constants.sentencedelimiters
        self._stopwords = constants.stopwords.default

    def set_delimiters(self, delimiters):
        self._sentencedelimiters = delimiters

    def set_stopwords(self, stopwords):
        self._stopwords = stopwords

    def delete_stopwords(self, words, stopwords=None):
        stopwords = stopwords if stopwords else self._stopwords
        try:
            words = [word for word in words if word.word not in stopwords]
        except AttributeError:
            words = [word for word in words if word not in stopwords]
        return words

    def text2para(self):
        pass

    def text2sentences(self, txt, punc=False):
        """
        cut a text into sentences using regex
        if punc is True then the ending punctuation will be kept
        """
        if punc:
            repl = r"\1\n"
        else:
            repl = "\n"
        return [s.strip() for s in re.sub(
            r"(%s)" % self._sentencedelimiters, repl, txt).split('\n')
            if s.strip() != '']

    def sentence2words(self):
        """
        segment sentence into words
        """
        raise NotImplementedError("Abstract method")

    def text2words(self, text, dim=2, pos=None, punc=False):
        """
        input:
            a text
        output:
            if dim is 2 return a 2 dimentional matrix
            if dim is 1 return a one dimentional one
        """
        corpus = []
        sentences = self.text2sentences(text)
        for sentence in sentences:
            corpus.append(self.sentence2words(sentence, pos=pos, punc=punc))
        return corpus

    def sentences2words(
        self,
        sentences,
        stopwords=True,
        pos=None,
        punc=False
    ):
        """return the sentences and corresponding corpus"""
        corpus = []
        for sentence in sentences:
            corpus.append(self.sentence2words(sentence, stopwords, pos, punc))
        sentences = [
            sentences[i] for i in range(len(corpus)) if corpus[i] != []]
        corpus = [
            corpus[i] for i in range(len(corpus)) if corpus[i] != []]
        assert len(sentences) == len(
            corpus), "sentence and corpus length not equal"
        return sentences, corpus

    def __call__(self):
        """
        """
        raise NotImplementedError("Abstract method")


class JiebaTokenizer(Tokenizer):
    def __init__(self):
        super(JiebaTokenizer, self).__init__()

    def sentence2words(
        self,
        sentence,
        stopwords=True,
        pos=None,
        punc=True
    ):
        """
        all possible pos tags for pos arg:
            ['an', 'i', 'j', 'l', 'n', 'nr', 'nrfg', 'ns',
             'nt', 'nz', 't', 'v', 'vd', 'vn', 'eng']
        inputs:
            sentence: the sentence which should be cut
            pos: part of speech, only listed POS will be returned
            include_stopwords: if is false all stopwords will be ignored and not
            returned
        return:
            a list of words returned
        """
        if not sentence:
            return None
        if isinstance(pos, list):
            words = posseg.cut(sentence)
            words = [w for w in words if w.flag in pos and w.word.strip()]
        elif pos is True:
            words = posseg.cut(sentence)
        elif pos is None:
            words = [word for word in jieba.cut(sentence) if word.strip()]

        if not stopwords:
            words = self.delete_stopwords(words)
        if not punc:
            try:
                words = [word for word in words if
                         word.word not in constants.punc]
            except AttributeError:
                words = [word for word in words if
                         word not in constants.punc]
        return words


class THUNLPTokenizer(Tokenizer):
    """
    all POS types:
        N/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
        m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
        v/动词 a/形容词 d/副词 h/前接成分 k/后接成分
        i/习语 j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
        e/叹词 o/拟声词 g/语素 w/标点 x/其它
    """
    def sentence2words(self, ):
        pass


cleanser = Cleanser()


def text2charlist(text, utf8=False):
    """
    return chinese character based list
    all word characters \w remain the same, not separated
    input:
        text can be both str or unicode, list or string
        coding will remain the same, if utf8 is true return utf-8
    """
<<<<<<< HEAD
    if sys.version_info >= (3, 0):
        _w = re.compile("(\w+)", re.A)
    else:
        _w = re.compile("(\w+)")

    flag = False
    if type(text) == list:
        text = [itm.decode('utf-8') if type(itm) == str else itm for itm in text]
        flag = True
        text = ''.join(text)
    elif type(text) == str:
        text = text.decode('utf-8')
        flag = True
    text = re.sub(_w, r' \1 ', text)
    lst = [[itm] if re.match('^\w+$', itm) else list(itm) for itm in cleanser.set_sentence(text).delete_whitespace().sentence.split()]
    text = ' '.join([' '.join(itm) for itm in lst])
    lst = [char for char in text.split() if char.strip() != ""]
    if flag and not utf8:
        lst = [char.encode('utf-8') for char in lst]
=======
    flag = False
    if type(text) == list:
        text = [itm if type(itm) == str else itm for itm in text]
        flag = True
        text = ''.join(text)
    elif type(text) == str:
        text = text
        flag = True
    text = re.sub(regex_compile("(\w+)"), r' \1 ', text)
    lst = [[itm] if re.match(regex_compile("^\w+$"), itm) else list(itm) for itm in cleanser.set_sentence(text).delete_whitespace().sentence.split()]
    text = ' '.join([' '.join(itm) for itm in lst])
    lst = [char for char in text.split() if char.strip() != ""]
    if flag and not utf8:
        lst = [char for char in lst]
>>>>>>> hubos/master
    return lst
