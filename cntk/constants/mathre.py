#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division

from cntk.utils import regex_compile

class Math2ZH(object):

    @staticmethod
    def frac():
        def sub_frac(match):
            if match.group('from'):
                return r"{den1}分之{num1}到{den2}分之{num2}".format(
                    **match.groupdict())
            elif match.group('to'):
                return r"{den2}分之{num2}".format(**match.groupdict())

        FRAC = {
            "pattern": regex_compile(
                "(?P<from>(?P<num1>\d+)/(?P<den1>\d+)[-~〜—一?])"
                "(?P<to>(?P<num2>\d+)/(?P<den2>\d+))"),
            "repl": sub_frac,
                "(?P<from>(?P<num1>\d+)/(?P<den1>\d+)[-~〜—一?])"
                "(?P<to>(?P<num2>\d+)/(?P<den2>\d+))"),
            "repl": sub_frac,
        }

        return FRAC

    @staticmethod
    def myint():
        INT = {
            "pattern": regex_compile("(\d+)\.0+[^\dloO]?"),
            "repl": r"\1",
        }

        return INT

    @staticmethod
    def zeroorone():
        """
        zero or one
        """
        def sub(match):
            lo = match.group("lo")
            lnum = match.group('lnum') or ''
            onum = match.group('onum') or ''
            if lo.lower().startswith('l'):
                repl = onum + len(lo) * '0'
            else:
                repl = len(lo) * '1' + lnum

            return repl

        ZOO = {
            "pattern": regex_compile(
                "(?<![0-9a-zA-Z])"
                "(?P<lo>[l]+(?P<lnum>\d)|(?P<onum>[1-9])[oO]+)"
            ),
            "repl": sub,
        }

        return ZOO

    @staticmethod
    def score():
        SCORE = {
            "pattern": regex_compile("(?<!\w)\d:\d(?!\w)"),
            "repl": r"\1比\2"
        }

        return SCORE

    @staticmethod
    def percent():
        PERCENT = {
            "pattern": regex_compile("(?<!\w)(\d+)\/(\d+)(?![\w\/])"),
            "repl": r"\2分之\1"
        }

        return PERCENT
