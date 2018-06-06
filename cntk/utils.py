#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division

import re
from codecs import open
from functools import reduce, wraps
from termcolor import colored


def regex_compile(regex, flags=[]):
    try:
        a = re.A
        r = re.compile(regex, reduce(lambda i,j: i|j, flags+[re.A], 0))
    except:
        a = 0
        r = re.compile(regex, reduce(lambda i,j: i|j, flags, 0))
    return r


def not_none(func):
    """
    decorator to make sure the sentence to be processed is not none
    this only validated on the middle level(utilization level)
    (rather thant on the constant or application level)
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            verbose = kwargs['verbose']
        except:
            verbose = False
        if verbose:
            func_name = func.__name__

        if self.is_none() and verbose:
            if verbose:
                print("Sentence is " + colored("NONE") + " before: '%s' in %s" % (self._sentence, func_name))
            return self
        else:
            if verbose:
                print("Before:\t '%s' ," % self._sentence)
            try:
                if 'verbose' in kwargs:
                    kwargs.pop("verbose")
                func(self, *args, **kwargs)
                if verbose:
                    print("After:\t'" + colored("%s" % self._sentence, 'red') + "' \nin %s function. \n" % func_name)
            except TypeError:
                raise
            return self
    return wrapper


def test_sub(sub_dic):
    """
    decorator to substitute
    if the sentence is None return self
    """
    def wrappers_wrapper(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.is_none():
                return self
            else:
                # print("safely sub: "+unicode(self._sentence))
                print("processed: "+func.__name__)
                self._sentence = re.sub(string=self._sentence, **sub_dic)
                return self
        return wrapper
    return wrappers_wrapper


def safely_sub(func):
    """
    decorator to substitute
    if the sentence is None return self
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            verbose = kwargs['verbose']
        except:
            verbose = False
        if verbose:
            func_name = func.__name__
        if self.is_none():
            if verbose:
                print("Sentence is " + colored("NONE") + " before: '%s' in %s" % (self._sentence, func_name))
            return self
        else:
            if verbose:
                print("Before:\t '%s' ," % self._sentence)
            self._sentence = re.sub(
                string=self._sentence, **func(self, *args, **kwargs))
            if verbose:
                print("After:\t'" + colored("%s" % self._sentence, 'red') + "' \nin %s function. \n" % func_name)
            return self
    return wrapper


def safely_del(offal_regex):
    def real_decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            try:
                verbose = kwargs['verbose']
            except:
                verbose = False
            if verbose:
                func_name = function.__name__
            if verbose:
                print("Before:\t '%s' ," % self._sentence)
            self._sentence = re.sub(
                offal_regex, '', self._sentence)
            for arg in args:
                self._sentence = re.sub(
                    arg, '', self._sentence)
            if verbose:
                print("After:\t'" + colored("%s" % self._sentence, 'red') + "' \nin %s function. \n" % func_name)
            return self
        return wrapper
    return real_decorator


def further_sub(sub_dic):
    def wrappers_wrapper(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                verbose = kwargs['verbose']
            except:
                verbose = False
            if verbose:
                func_name = func.__name__
            if self.is_none():
                if verbose:
                    print("Sentence is " + colored("NONE") + " before: '%s' in %s" % (self._sentence, func_name))
                return self
            if verbose:
                print("Before:\t '%s' ," % self._sentence)
            self._sentence = re.sub(string=self._sentence, **sub_dic)
            if verbose:
                print("After:\t'" + colored("%s" % self._sentence, 'red') + "' \nin %s function. \n" % func_name)
            return self

        return wrapper

    return wrappers_wrapper


def debug(func):
    """
    decorator to debug
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        import time
        # print("sentence before %s processing: %s" % (
        #     unicode(func.__name__), unicode(self._sentence)))
        # print("to be "+unicode(func.__name__))
        time.sleep(2)
        try:
            func(self, *args, **kwargs)
            # print("sentence after %s processing: %s" % (
            #     unicode(func.__name__), unicode(self._sentence)))
            # print('\n\n')
            time.sleep(2)
            return self
        except:
            print(func.__name__)
            raise
    return wrapper


def safe_log(func):
    """
    write down the sentence if in the function it is deleted
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_none():
            return self
        else:
            func(self, *args, **kwargs)
            if self.is_none():
                with open("deleted_lines", "a", "utf-8") as savor_file:
                    savor_file.write(
                        self.origin_sentence + u" # %s \n" % self.reason)
                # why?
        return self
    return wrapper


class AttrDict(dict):
    """Dict that can get attribute by dot"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# source: http://stackoverflow.com/a/14620633/3552975


class BaseProcessor(object):
    """
    A base class for all kinds of processors
    """
    def __init__(self, sentence):
        self._sentence = sentence

    def __str__(self):
        return self._sentence

    def set_sentence(self, sentence):
        self._sentence = sentence
        return self

    def is_none(self):
        return not bool(self._sentence)

    @property
    def sentence(self):
        return self._sentence
