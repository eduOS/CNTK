#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division


class Brand_en2zh(object):

    brands = {
        # "iphone": "苹果",
        "twitter": "推特",
        "tweetbot": "推特客户端",
        "galaxy": "盖乐世",
        "bigbang": "大爆炸乐团",
        "casa milan": "米兰之家",
        "skyfall": "大破天幕杀机",
        "mac mini": "苹果迷你",
        "macbook": "苹果笔记本",
        "ubuntu": "乌班图",
        "titanic": "泰坦尼克",
        "disney": "迪士尼",
        "louis vuitton": "路易威登",
        "gucci": "古驰",
        "Adidas": "阿迪达斯",
        "Seiko": "精工",
        "coca[- ]?cola": "可口可乐",
        "mcdonald’?s?": "麦当劳",
        "heineken": "喜力",
        "bmw": "宝马",
        "volkswagen": "大众汽车",
        "porsche": "保时捷",
        "ikea": "宜家",
        "johnson( & johnson)?": "强生",
        "bosch": "博世",
        "akon": "阿肯",
        "google": "谷歌",
    }

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
