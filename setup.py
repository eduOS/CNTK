#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from setuptools import setup

setup(
    name='cntk',
    packages=['cntk', 'cntk.constants'],
    version='0.0.1',
    description='CNTK: a Chinese processing toolkit',
    author='Lerner Adams',
    author_email='lerner.adams@hotmail.com',
    # url='https://github.com/kedz/sumpy',
    install_requires=["jieba", "opencc", "html2text", "termcolor, pyhanlp"],
    # include_package_data=True,
)
