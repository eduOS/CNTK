#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from unicodedata import normalize


class Punctuation(object):

    # A string containing Chinese punctuation marks (non-stops).
    ZH_NON_STOPS = (
        # Fullwidth ASCII variants
        '＂＃＄￥％＆＇`（）＊＋，－'
        '／：；＜＝＞＠［＼］＾＿'
        '｀｛｜｝～｟｠'

        # Halfwidth CJK punctuation
        '「」｢｣､ ﹁﹂'

        # CJK symbols and punctuation
        '　、〃'

        # CJK angle and corner brackets
        '〈〉《》「」『』【】'

        # CJK brackets and symbols/punctuation
        '〔〕〖〗〘〙〚〛〜〝〞〟'

        # Other CJK symbols
        '〰'

        # Special CJK indicators
        # '〾〿'

        # Dashes
        '–—'

        # Quotation marks and apostrophe
        '‘’‛“”„‟'

        # General punctuation
        '…‧'

        # Overscores and underscores
        '﹏'

        # Small form variants
        '﹑﹔'

        # Latin punctuation
        '·'

        "°﹐・•"
    )

    PERIODS = ".．｡。"

    HALF_ZH_NON_STOPS = normalize('NFKC', ZH_NON_STOPS)

    ZH_LEFT_PAIRED = "‘“〈《「『【﹁｢｟（＜［｛〔〖〘〚〝"
    ZH_RIGHT_PAIRED = "’”〉》」』】﹂｣｠）＞］｝〕〗〙〛〞"

    HALF_ZH_LEFT_PAIRED = normalize('NFKC', ZH_LEFT_PAIRED)
    HALF_ZH_RIGHT_PAIRED = normalize('NFKC', ZH_RIGHT_PAIRED)

    #: A string of Chinese stops.
    ZH_STOPS = (
        '！'  # Fullwidth exclamation mark
        '？'  # Fullwidth question mark
        '｡'  # Halfwidth ideographic full stop
        '。'  # Ideographic full stop
        # the following are western ones
    )

    HALF_ZH_STOPS = normalize('NFKC', ZH_STOPS)

    #: A string containing all Chinese punctuation.
    ZH_ALL = ZH_NON_STOPS + ZH_STOPS
    HALF_ZH_ALL = HALF_ZH_NON_STOPS + HALF_ZH_STOPS

    EN_NON_STOPS = (
        "|~_"
        "’'"  # apostrophe
        "<>[](){}⟨⟩"  # brackets
        ":"  # colon
        ",،、"  # comma
        "‒ ―"  # dash
        "‹›«»"  # guillemets
        "‐"  # hyphen
        "-"  # hyphen-minus
        """‘’"“”'"""  # quotation marks
        ";"  # semicolon
        "/⁄"  # slash, stroke, solidus
        "@"
    )

    # the following punctuations are according to wikipedia
    EN_STOPS = (
        '!'
        '﹗'
        '?'
        '.'
        "．"  # full stop
        '…'
    )

    LEFT_COMMENT_MARKS = "[【｟〔〖〘〚\[{(（]"
    RIGHT_COMMENT_MARKS = "[】｠〕〗〙〛\]})）]"
    COMMENT = LEFT_COMMENT_MARKS + ".*?" + RIGHT_COMMENT_MARKS

    # the following two strings are for transition between English
    # and Chinese punctuation
    ZH_PUNC = (
        '。|？|！|，|、|；|：|“|”|‘|’|'
        '（|）|［|］|【|】|《|》|〈|〉|─|―|－|～|＿|…|—|﹏|–'
    )

    EN_PUNC = (
        """.|?|!|,|,|;|:|"|"|'|'|(|)|[|]|[|]|<|>|<|>|-|-|-|~|_|.|-|_|-""")
    # TODO tell if " is “ or ” and so for '

    USELESS = (
        """([�®—‧′↑→↓∙⋯▍□▲○●、〇〡・█■`△｀:/|()\[\]{}「〜•」『』'<>\-\~_·#]+|"""
        """(?<=[,.])[.,]+|\\[nr]|(?<=\?)\?+|=.=)"""
    )

    EN_NON_STOP_END = '°>’"”)}›»'
    EN_SENTENCE_END = EN_NON_STOP_END + EN_STOPS
    EN_SENTENCE_START = """‹«‘"“'⟨"""

    # the following are for all characters

    # all stops
    STOPS = EN_STOPS + ZH_STOPS
    # all punctuations that are not the stops
    NON_STOPS = EN_NON_STOPS + ZH_NON_STOPS
    # all of the punctuations
    ALL = STOPS + NON_STOPS
    # these punctuations may be at the end of the sentence but not stops
    # NON_STOP_END = EN_NON_STOP_END + ZH_NON_STOP_END
    # these punctuations may be at the end of an English sentence
    # SENTENCE_END = EN_SENTENCE_END + ZH_SENTENCE_END
    # these punctuations may be at the start of a sentence
    # SENTENCE_START = EN_SENTENCE_START + ZH_SENTENCE_START
    SENTENCE_DELIMITERS = (
        "[．.]{2,}(?=\d)|[\t\n\r！？｡。；\|；;~!﹗?…]+|[．.]+(?=([^\d]|$))|(?<=[\u4e00-\u9fff])[．.]+|(?<=\d)[．.](?!\d)"
    )
    EN_SENTENCE_DELIMITERS = EN_STOPS + """[]<>|;{}｛｝~\t\n\r"""
    ZH_SENTENCE_DELIMITERS = ZH_STOPS + """；【】\t\n\r"""
    # SENTENCE_DELIMITERS = EN_SENTENCE_DELIMITERS + ZH_SENTENCE_DELIMITERS

    NOTALLOWDED = (
        """(?<=[a-zA-Z0-9])"""
        """(!|"|""|'|\.|\/\.|\/\/|\:|\:"|\:\/\/|\:\:|\;|\?|\{|\})"""
        """(?=[a-zA-Z0-9])"""
    )
    ALL_PUNC = (
        # for copy and paste only
        # the same can be imported by Punctuation.ALL
        """＂— #＃＄￥%％&＆＇（）＊＋，－／：；＜＝＞@＠［＼］＾＿｀｛｜｝～｟｠"""
        """「」｢｣､﹁﹂　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟"""
        """〰–—‘’‛„‟…‧﹏﹑﹔·°﹐・•|~_’'<>[](){}⟨⟩:,،、‒―‹›«»‐-‘’"“”;/⁄"""
        """!﹗?.．…！？｡。"""
    )


ALL_PUNC = (
    # for copy and paste only
    # the same can be imported by Punctuation.ALL
    """＂＃＄￥％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠"""
    """「」｢｣､﹁﹂　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟"""
    """〰–—‘’‛“”„‟…‧﹏﹑﹔·°﹐・•|~_’'<>[](){}⟨⟩:,،、‒―‹›«»‐-‘’"“”;/⁄@"""
    """!﹗?.．…！？｡。"""
)
