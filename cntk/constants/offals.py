#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division

from cntk.constants.punctuation import Punctuation

BULLET = (
    "("
    "^\s*[第其]?[0-9０１２３４５６７８９一二三四五六七八九]+([/\])?"
    "([-、，,:：．　\)）]|(\.(?!\d))|个?就?是)"
    "|"
    "^[A-D]\."
    ")"
)
PARENOTE = Punctuation.COMMENT

ADDITION = "[Pp][Ss][:： ]"

OTHERS = (
    "^("
    "另一.{,3}是|.{1,4}[:：]|"
    "版本.?[:：]|修正[:：]|以至于?"
    ")"
)

FORWARD = "\/*\@.*?(:|\t| |：)"

# LINK = '\s*(?:https?://)?www\.\S*\.[A-Za-z]{2,5}\s*'
LINK = (
    "[（(]http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|"
    "(?:%[0-9a-fA-F][0-9a-fA-F]))+[)）]"
)
# source: https://mathiasbynens.be/demo/url-regex

DIGITS = '[0-9.]+'

CONJUNCTION = (
    # reference: http://baike.baidu.com/item/%E8%BF%9E%E8%AF%8D/505099

    # transition
    "^([可但只]是|否则|不然|却|虽然|然而|而|偏偏|只?不过|不料|岂知|"
    "反之亦然|.*答案就?是|希望.*有用$|.*[一二三四五六七八九]:"
    # coordination
    "况且|更?何况|乃至|当然|"
    # continuing
    "还有|于是|然后|至于(为什么)?|说到|[此另]外|接着|加上|"
    "从这|其[次他]|后来|[而并]且|比如|这样|相比(之下)?|"
    "比如说|回到|说一下|说了|(?P<qi>其)[二三四](?(qi)|就?是)|"
    # progressive
    "不但|不仅|[而并]?且|何况|"
    "加之|另：|同时|另外(一方面)?|于是|"
    # causality
    "所以说?|原来|因为|由于|以便|因此|是故|以致|"
    # hypothesis
    # "若是|假如|假使|倘若|即使|假若|要是|"
    # alternative
    "或者?说?|亦|即(?!使)|"
    # concessive
    "虽然|固然|尽管|纵然"
    ")"
    # comparative
    # "像|好比|如同|似乎|等于|不如|不及|与其…不如|若…则|虽然…可是"
    # connective
    # "不管|只要|除非"
    # objective
    # "以|以便|以免|为了"
)
