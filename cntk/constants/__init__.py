"""
Provides CC-CEDICT character constants.
reference url = https://github.com/tsroten/zhon
"""

from __future__ import unicode_literals

from . import leetspeak, coarse_language, punctuation, cjk, stopwords, offals, keywords

__all__ = ['simp', 'trad', 'tradsimp', 'leet', 'coarse', 'cjk', 'punc',
           'stops', 'nonstops', 'sentencestart', 'sentenceend', 'nonstopend',
           'nonsense', 'sentencedelimiters_en', 'sentencedelimiters',
           'sentencedelimiters_zh', 'enpunc', 'zhpunc', 'stopwords', 'bullets',
           'additions', 'puzzle_kws', 'product_kws', 'other_kws'
           ]

all_pos = [
    "Ag", "a", "ad", "an", "b", "c", "dg", "d", "e", "f",
    "g", "h", "i", "j", "k", "l", "m", "Ng", "n", "nr", "ns",
    "nt", "nz", "o", "p", "q", "r", "s", "tg", "t", "u", "vg",
    "v", "vd", "vn", "w", "x", "y", "z", "un"
]

#: A string containing all Simplified characters according to CC-CEDICT.
simp = simplified = cjk.SIMPLIFIED_CHINESE

#: A string containing all Traditional characters according to CC-CEDICT.
trad = traditional = cjk.TRADITIONAL_CHINESE

#: A string containing all Chinese characters found in CC-CEDICT.
tradsimp = cjk.TRADSIMP_CHINESE

#: A string containing only leetspeak characters
leet = leetspeak = ''.join(list(set(leetspeak.CHARACTERS) - set(tradsimp)))

#: A string containing all coarse language
coarse = coarselanguage = coarse_language.CHARACTERS

#: A unicode range containing all cjk words
cjk = cjk.ALL_CJK

#: A string containing all punctuation
punc = punctuation.Punctuation.ALL
# stops = punctuation.STOPS
# nonstops = punctuation.NON_STOPS
# sentenceend = punctuation.SENTENCE_END
# sentencestart = punctuation.SENTENCE_START
# nonstopend = punctuation.NON_STOP_END
# nonsense = punctuation.NON_SENSE
sentencedelimiters = punctuation.Punctuation.SENTENCE_DELIMITERS
# sentencedelimiters_en = punctuation.EN_SENTENCE_DELIMITERS
# sentencedelimiters_zh = punctuation.ZH_SENTENCE_DELIMITERS
#
# #: the transition pair
# enpunc = punctuation.EN_PUNC.split("|")
# zhpunc = punctuation.ZH_PUNC.split("|")
stopwords = stopwords
bullets = offals.BULLET
additions = offals.ADDITION
parenote = offals.PARENOTE
link = offals.LINK

puzzle_kws = keywords.MULTICHOICE_KWS
product_kws = keywords.PRODUCT_KWS
other_kws = keywords.OTHERKEYWORDS
multimedia_kws = keywords.MULTIMEDIA
number_kws = keywords.NUMBER_KWS
