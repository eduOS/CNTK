#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

# including all about characters about week
week = '[下这]+(星期|周)[一二三四五六七天日末]?'
time = '([上下中]午|晚上|早晨)?\d{,4}[一二三四五六七八九十]{,5}点?半?'
# the short relate time
relatime = '现在'  # 1320
relaDate = '[今明后当]天?'  # cover all relative date  36310
# the absolute date detailed from year to day
# 23643

absoDate = (
    "\d{,4}[一二三四五六七八九十]{,5}[明下今]?年?"
    "\d{,2}[一二三四五六七八九十]{,4}[下这]?个?月?"
    "\d{,2}[一二三四五六七八九十]{,4}[号日]"
)

relaTime = (
    "(?P<time>(" +
    relaDate +
    '|' +
    week +
    '|' +
    relatime +
    ')' +
    time +
    ')'
)

absoTime = '(?P<time>' + absoDate + time + ')'

EN_DATE = "(?P<year>\d{4})\.(?P<month>[01]?\d)\.(?P<day>[0123]\d)"
TIME_RANGE = "(?<=\d{1,4}[年月日]?)([?\-~〜~—])+(?=\d{1,4}[年月日])"


class Time2ZH(object):

    @staticmethod
    def zero():
        def sub(match):
            return len(match.group('o0')) * "零"

        FRAC = {
            "pattern": (
                "(?<=[一二三四五六七八九十])"
                "(?P<o0>[oO0]+)(?=[一二三四五六七八九十])"
            ),
            "repl": sub,
        }

        return FRAC
