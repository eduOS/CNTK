#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
import re


class Unit2ZH(object):
    """
    several parts to modify:
        1. units
        2. range
    """

    pairs4sure = {
        # if following digits these are clear to be units
        "GHz": "吉赫兹",
        "KHz": "千赫兹",
        "MHz": "兆赫兹",
        "Hz": "赫兹",
        "mΩ": "兆欧姆",
        "Ω": "欧姆",
        "Kpa": "千帕斯卡",
        "pa": "帕斯卡",
        "KB": "千比特",
        "MB": "兆比特",
        "Byte": "比特",
        "Gb": "吉比特",
        "bit": "比特",
        "mG": "毫克",
        "mL": "毫升",
        "mV": "毫伏",
        "mml": "毫升",
        "mmol": "毫摩尔",
        "mol": "摩尔",
        "ml": "毫升",
        "mm": "毫米",
        "mmHg": "毫米汞银柱",
        "cm": "厘米",
        "nm": "纳米",
        "oC": "摄氏度",
        "s": "秒",
        "segma": "西格玛",
        "um": "微米",
        "KW": "千瓦特",
        "MW": "兆瓦",
        "KJ": "千焦",
        "mJ": "兆焦",
        "Kbps": "位秒",
        "Mev": "兆电子伏特",
        "lux": "勒克斯",
        "dm": "分米",
        "hm": "公顷",
        "kg": "千克",
        "km": "千米",
        "kV": "千伏",
        "cfu": "细菌群落每平方米",
        "l": "1",
        "d": "天"
    }

    ambipairs = {
        # ambiguous pairs
        "L": "升",
        "t": "顿",
        "V": "伏特",
        "W": "瓦",
        "m": "米",
    }

    betweenChinese = {
        # if following digits these are clear to be units
        "GHz": "吉赫兹",
        "KHz": "千赫兹",
        "MHz": "兆赫兹",
        "Hz": "赫兹",
        "mΩ": "兆欧姆",
        "Ω": "欧姆",
        "Kpa": "千帕斯卡",
        "pa": "帕斯卡",
        "KB": "千比特",
        "MB": "兆比特",
        "Byte": "比特",
        "Gb": "吉比特",
        "bit": "比特",
        "mG": "毫克",
        "mL": "毫升",
        "mV": "毫伏",
        "mml": "毫升",
        "mmol": "毫摩尔",
        "mol": "摩尔",
        "ml": "毫升",
        "mm": "毫米",
        "mmHg": "毫米汞银柱",
        "cm": "厘米",
        "nm": "纳米",
        "oC": "摄氏度",
        "s": "秒",
        "segma": "西格玛",
        "um": "微米",
        "KW": "千瓦特",
        "MW": "兆瓦",
        "KJ": "千焦",
        "mJ": "兆焦",
        "Kbps": "位秒",
        "Mev": "兆电子伏特",
        "lux": "勒克斯",
        "dm": "分米",
        "hm": "公顷",
        "kg": "千克",
        "km": "千米",
        "kV": "千伏",
        "cfu": "细菌群落每平方米",
    }

    @staticmethod
    def myrange():
        """
        space should be deleted
        """
        def range_sub(match):
            return r"{from}到{to}".format(**match.groupdict())
        RANGE = {
            "pattern": (
                "(?P<from>\d"
                "[°a-zA-Z\u4e00-\u9fff]{0,7}(?:[23])?"
                "(?:\/[a-zA-Z\u4e00-\u9fff]+[23]?)?)"
                "[-~〜—一?]+"  # full width ～一 ~〜~—
                "(?P<to>\d(?:\.\d)?[\d:]*"
                "(?:[°a-zA-Z\u4e00-\u9fff]{1,7})(?:[23])?"
                "(?:\/[a-zA-Z\u4e00-\u9fff]+[23]?)?)"),
            "repl": range_sub,
        }
        return RANGE

    @staticmethod
    def extractor():
        """
        extract units
        """
        EXTRACTOR = (
            "(?<=([\u4e00-\u9fff]|^))"
            "(?:\d(\.\d)?\d*)"
            # match the numbers ahead of the units
            "(?P<unit>[°a-zA-Z]{1,5}([23])?"  # match the base units
            "(\/[a-zA-Z]+[23]?)?)"
            # if a forward slash is appended then continue matching
            "(?=([\u4e00-\u9fff]|$))"
            # make sure that only Chinese characters and the end mark is
            # followed
        )
        return EXTRACTOR

    @staticmethod
    def percent():
        def percent_sub(match):
            if match.group("thou"):
                p = "千"
            elif match.group("hun"):
                p = "百"

            to = match.group('to')
            if match.group('range'):
                fr = match.group('from')
                return p+"分之"+fr+"到"+p+"分之"+to
            elif match.group('to'):
                return p+"分之"+to
            # http://stackoverflow.com/a/17476793/3552975

        PERCENT = {
            # some problems here
            "pattern": (
                # "(?P<range>(?P<from>[\d\.]+)((?P<thou>‰)|(?P<hun>\%))?"
                # "[?\-～ ~〜~—])?(?P<to>[\d\.]+)"
                # "(?:(?(thou)(?P<thou1>‰)|(?(hun)(?P<hun1>\%)|(?!))))"
                "(?P<range>(?P<from>[\d.]+)[‰%]?"
                "[-~〜—一?])?(?P<to>[\d.]+)"
                # should delete here
                "(?:(?P<thou>‰)|(?P<hun>\%))"
            ),
            "repl": percent_sub,
        }

        return PERCENT

    @staticmethod
    def time():
        def time_sub(match):
            amp = match.group('apm')
            fbd = match.group('fbd')
            if fbd and amp:
                amp = r"上午" if amp.startswith('a') else "下午"
            elif fbd:
                return fbd + "{hour}比{minu}".format(**match.groupdict())
            elif amp:
                amp = r"上午" if amp.startswith('a') else "下午"
            else:
                amp = r""
            # the default is to treat the pattern as a time
            return amp+"{hour}点{minu}分".format(**match.groupdict())

        TIME = {
            'pattern': (
                "(?P<fbd>[成是为按比以])?"
                "((?P<hour>[01]\d|2[0-3]):(?P<minu>[0-5]\d)|24:00)"
                "(?P<apm>[ap]\.?m\.?)?"
            ),
            'repl': time_sub
        }
        return TIME

    @staticmethod
    def date():
        def date_sub(match):
            if match.group('day'):
                return r"{year}年{month}月{day}日".format(**match.groupdict())
            elif match.group('month'):
                return r"{year}年{month}月".format(**match.groupdict())

        DATE = {
            "pattern": (
                "(?P<year>(1[7-9]|20)\d{2})[-./]"
                "(?P<month>((?P<mf>0)|[12])?(?(mf)[1-9]|\d*))"
                "(?:[-./])?(?P<day>((?P<df>0)|[1-3])?(?(df)[0-9]|\d*))?"
            ),
            "repl": date_sub,
        }

        return DATE

    @staticmethod
    def per():
        def per_sub(match):
            return r"{num}每{deno}".format(**match.groupdict())

        PER = {
            "pattern": (
                "(?P<num>\d(\d|\.)*[\u4e00-\u9fff]{,3})"
                "\/(?P<deno>[\u4e00-\u9fff]{1,3})"),  # the full width ／
            "repl": per_sub,
        }

        return PER

    @staticmethod
    def pon(match):
        """
        positive or negtive
        """
        if match.group('pon') == '-':
            return "负"
        elif match.group('pon') == '+':
            return "正"
        else:
            return ""

    @staticmethod
    def latnlon():
        '''
        latitude and longitude
        '''
        def latnlon_sub(match):
            pref = Unit2ZH.pon(match)

            deg = match.group('deg')
            minu = match.group('minu')
            sec = match.group('sec')

            if sec:
                rt = deg+"度"+minu+"分"+sec+"秒"
            elif minu:
                rt = deg+"度"+minu+"分"
            elif deg:
                rt = deg+"度"
            return pref+rt

        ANGLE = {
            "pattern": (
                "(?P<pon>[-+])?(?P<deg>[\d\.]+)°"
                """((?P<minu>\d+)[′'])?((?P<sec>\d+)(′′|"))?(?![C])"""
                # the full width is ′＇ and ″＂
            ),
            "repl": latnlon_sub,
        }

        return ANGLE

    @staticmethod
    def temp():
        def temp_sub(match):
            pon = Unit2ZH.pon(match)
            num = match.group('num') or ''
            # deg = match.group('deg')
            u = match.group('unit')
            unit = '度'
            type = ''
            if not u or u.lower() == 'c':
                type = '摄氏'
                # the default is centigrade
            elif u.lower() == 'f':
                type = '华氏'
            elif u.lower() == 'k':
                unit = '开尔文'
            # elif unit.lower().startswith('c'):
            #        type = '摄氏'
            return pon + type + num + unit

        TEMP = {
            "pattern": (
                "(?P<pon>[-+])?(?P<num>([\.\d]+))?°(?P<unit>[cfk])"
                # "(?![^\w])"
            ),
            # ℃   is the full width character of °C
            "repl": temp_sub,
            "flags": re.IGNORECASE
        }

        return TEMP

    @staticmethod
    def unit_en2zh0():
        """
        units for sure not in any conditions
        """

        def sub(match):
            unit = match.group('unit')
            try:
                nrep = Unit2ZH.pairs4sure[unit]
            except KeyError:
                nrep = unit

            return nrep

        UNIT = {
            "pattern": ("(?<=[\u4e00-\u9fff])"
                        "(?P<unit>[a-zA-Z]+)(?=[\u4e00-\u9fff\.])"),
            "repl": sub,
            "flags": re.IGNORECASE
        }

        return UNIT

    @staticmethod
    def unit_en2zh1():
        """
        units for sure not in any conditions
        """

        def en_sub(match):

            try:
                n23 = match.group('n23')
                if n23 == '2':
                    n23 = "平方"
                elif n23 == '3':
                    n23 = "立方"
                else:
                    n23 = ""
            except:
                n23 = ""

            if match.group('derived'):
                num = match.group('num')

                d23 = match.group('d23')
                if d23 == '3':
                    d23 = "立方"
                if d23 == "2":
                    d23 = "平方"
                else:
                    d23 = ""

                try:
                    nrep = Unit2ZH.pairs4sure[num]
                except KeyError:
                    nrep = num

                dem = match.group('dem')
                try:
                    drep = Unit2ZH.pairs4sure[dem]
                except KeyError:
                    drep = dem

                return n23 + nrep + "每" + d23 + drep

            elif match.group('num'):
                num = match.group('num')
                try:
                    nrep = Unit2ZH.pairs4sure[num]
                except KeyError:
                    nrep = num
                return n23 + nrep

        UNIT = {
            "pattern": (
                "(?<=\d)(?P<num>[a-zA-Z]+)(?P<n23>[23])?"
                "(?P<derived>/(?P<dem>[a-zA-Z]+)(?P<d23>[23])?)?"
            ),
            "repl": en_sub,
            "flags": re.IGNORECASE
        }

        return UNIT

    @staticmethod
    def unit_en2zh2():
        """
        for units in certain type 2 with more restrictions
        """

        def en2zh_sub(match):
            if match.group('ton'):
                return "顿"
            if match.group('o20'):
                return "0" * len(match.group('o20'))
            if match.group('vt'):
                return "伏特"
            if match.group('mul'):
                return "乘以"

        EN2ZH = {
            "pattern": (
                "(?<=\d)"
                "((?P<ton>t(?!\w))|"
                "((?P<o20>[Oo]+)(?=[\u4e00-\u9fff]))|"
                "((?P<vt>V)(?!\w))|"
                "((?P<mul>X)(?=\d)))"
            ),
            "repl": en2zh_sub,
            "flags": re.IGNORECASE
        }

        return EN2ZH

    @staticmethod
    def unit_en2zh3():
        """
        for units with restrictions
        """

        en2zh = {}
        en2zh.update(Unit2ZH.ambipairs)
        en2zh.update(Unit2ZH.pairs4sure)

        def en_sub(match):

            try:
                n23 = match.group('n23')
                if n23 == '2':
                    n23 = "平方"
                elif n23 == '3':
                    n23 = "立方"
                else:
                    n23 = ""
            except:
                n23 = ""

            if match.group('derived'):
                num = match.group('num')

                d23 = match.group('d23')
                if d23 == '3':
                    d23 = "立方"
                if d23 == "2":
                    d23 = "平方"
                else:
                    d23 = ""

                try:
                    nrep = en2zh[num]
                except KeyError:
                    nrep = num

                dem = match.group('dem')
                try:
                    drep = en2zh[dem]
                except KeyError:
                    drep = dem

                return n23 + nrep + "每" + d23 + drep

            elif match.group('num'):
                num = match.group('num')
                try:
                    nrep = Unit2ZH.pairs4sure[num]
                except KeyError:
                    nrep = num
                return n23 + nrep

        DERIVED = {
            "pattern": (
                "(?<=\d)(?P<num>[a-zA-Z]+)(?P<n23>[23])?"
                "(?P<derived>/(?P<dem>[a-zA-Z]+)(?P<d23>[23])?)?"
            ),
            "repl": en_sub,
            "flags": re.IGNORECASE
        }

        return DERIVED
