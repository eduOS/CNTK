#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
import os
import jieba
import codecs
import collections

__all__ = ['get_stopwords_from_dir']


def get_stopwords_from_dir(din, no):
    """
    input:
        din: the directory containing files to get the stop words, can be very
        big
        no: the top no words
    output:
        return the top no words as stopwords
    """
    if not din.endswith("/"):
        din += "/"
    wct = collections.Counter()

    with codecs.open("./zhstopwds.txt", "r", 'utf-8') as f:
        zhstopwds = [word.strip() for word in f.readlines()]

    for file in os.listdir(din):
        if os.path.isfile(din+file):
            with codecs.open(din+file, "r", 'utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() != "":
                        wct.update(jieba.cut(''.join(line), cut_all=False))

    return [i[0] for i in wct.most_common(no) if i[0] not in zhstopwds]
