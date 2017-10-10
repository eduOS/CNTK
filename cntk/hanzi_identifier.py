# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
import re

from cntk import constants

UNKNOWN = 0
TRAD = TRADITIONAL = 1
SIMP = SIMPLIFIED = 2
BOTH = 3
MIXED = 4

_TRADITIONAL_CHARACTERS = set(constants.traditional)
_SIMPLIFIED_CHARACTERS = set(constants.simplified+constants.punc)
_SHARED_CHARACTERS = _TRADITIONAL_CHARACTERS.intersection(
    _SIMPLIFIED_CHARACTERS)
_BOTH_TRADANDSIMP = set(constants.tradsimp)
_LEETSPEAK_CHARACTERS = set(constants.leet)
_COASELANG = set(constants.coarselanguage)
_cjk = constants.cjk
_punc = constants.punc

__all__ = ['has_chinese', 'identify',
           'has_chinese', 'has_only_chinese',
           'has_non_cjk', 'has_leetspeak',
           'has_coarselanguage', 'is_simplified',
           'is_traditional', 'is_leetspeak'
           ]
# can I put the compiled regex outside functions to save time?
# transimp = re.compile('[%s]' % ''.join(_BOTH_TRADANDSIMP))

re_non_chinese = re.compile("[^%s]" % "".join(_BOTH_TRADANDSIMP))
re_all_chinese = re.compile('[%s]' % ''.join(_BOTH_TRADANDSIMP))
re_non_leetspeak = re.compile('[^%s]' % "".join(_LEETSPEAK_CHARACTERS))
re_non_cjk = re.compile("[^%s]" % _cjk)
re_coaselanguage = re.compile("|".join(_COASELANG))


def _get_hanzi(s):
    """Extract a string's Chinese characters."""
    return set(re.sub(re_non_chinese, '', s))


def _get_non_chinese(s):
    """
    extract a string's non chinese characters
    """
    return set(re.sub(re_all_chinese, '', s))


def _get_only_traditional(s):
    """Extract a string's tranditional characters only,
    no shared characters inclued"""
    return _get_hanzi(s) - _SIMPLIFIED_CHARACTERS


def has_traditional(s):
    """Check if a string has traditional characters in it."""
    return bool(_get_only_traditional(s))


def _get_leetspeak(s):
    """Extract a string's leetspeak characters."""
    return set(re.sub(re_non_leetspeak, '', s))


def _get_cjk(s):
    """
    Extract a strings non cjk characters
    """
    return set(re.sub(re_non_cjk, '', s))


def _get_english_word_characters(s):
    """
    Extract a string's english word characters [a-zA-Z0-9_]
    """
    return set(re.sub("[^a-zA-Z0-9_]", '', s))


def _get_punctuations(s):
    """
    Extract a string's punctuations
    NB: remember to escape the . and others as constants
    """
    return set(re.sub("[^%s]" % re.escape(_punc), "", s))


def identify(s):
    """Identify what kind of Chinese characters a string contains.

    *s* is a string to examine. The string's Chinese characters are tested to
    see if they are compatible with the Traditional or Simplified characters
    systems, compatible with both, or contain a mixture of Traditional and
    Simplified characters. The :data:`TRADITIONAL`, :data:`SIMPLIFIED`,
    :data:`BOTH`, or :data:`MIXED` constants are returned to indicate the
    string's identity. If *s* contains no Chinese characters, then
    :data:`UNKNOWN` is returned.

    All characters in a string that aren't found in the CC-CEDICT dictionary
    are ignored.

    Because the Traditional and Simplified Chinese character systems overlap, a
    string containing Simplified characters could identify as
    :data:`SIMPLIFIED` or :data:`BOTH` depending on if the characters are also
    Traditional characters. To make testing the identity of a string easier,
    the functions :func:`is_traditional`, :func:`is_simplified`, and
    :func:`has_chinese` are provided.

    """
    chinese = _get_hanzi(s)
    if not chinese:
        return UNKNOWN
    if chinese.issubset(_SHARED_CHARACTERS):
        return BOTH
    if chinese.issubset(_TRADITIONAL_CHARACTERS):
        return TRADITIONAL
    if chinese.issubset(_SIMPLIFIED_CHARACTERS):
        return SIMPLIFIED
    return MIXED


def has_chinese(s):
    """Check if a string has Chinese characters in it.

    This is a faster version of:
        >>> identify('foo') is not UNKNOWN

    """
    return bool(_get_hanzi(s))


def has_only_chinese(s):
    """
    Check if a string has only Chinese(numbers no longer than 5 and punctuations
    can be contained)
    return bool()
    """
    if re.match('[0-9]{5,}', s):
        return False
    s = re.sub('[0-9]', '', s)
    return not bool(_get_non_chinese(s) - _get_punctuations(s))


def has_non_cjk(s):
    """
    and except punctuations and english word characters
    """
    NON_CJK = set(s) - _BOTH_TRADANDSIMP - _get_cjk(s)
    return bool(
        NON_CJK - _get_english_word_characters(s) - _get_punctuations(s)
    )


def has_leetspeak(s):
    """Check if a string has leetspeak characters in it.
    """
    return bool(_get_leetspeak(s) - _get_hanzi(s))


def has_coarselanguage(s):
    """
    check if a string has coarselanguage in it.
    improvement:
    https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s09.html
    """
    # return any(coarse in s for coarse in _COASELANGUE)
    return bool(re.search(re_coaselanguage, s))


def is_traditional(s):
    """Check if a string's Chinese characters are Traditional.

    This is equivalent to:
        >>> identify('foo') in (TRADITIONAL, BOTH)

    """
    chinese = _get_hanzi(s)
    if not chinese:
        return False
    elif chinese.issubset(_SHARED_CHARACTERS):
        return True
    elif chinese.issubset(_TRADITIONAL_CHARACTERS):
        return True
    return False


def is_simplified(s):
    """Check if a string's Chinese characters are Simplified.

    This is equivalent to:
        >>> identify('foo') in (SIMPLIFIED, BOTH)

    """
    chinese = _get_hanzi(s)
    if not chinese:
        return False
    elif chinese.issubset(_SHARED_CHARACTERS):
        return True
    elif chinese.issubset(_SIMPLIFIED_CHARACTERS):
        return True
    return False


def is_leetspeak(s):
    """Check if a string's characters are leetspeak characters.
    """
    leetspeak = _get_leetspeak(s)
    if not leetspeak:
        return False
    elif leetspeak.issubset(_BOTH_TRADANDSIMP):
        return False
    return True


def get_ch_ratio(s, illegal="[a-zA-Z]"):
    legal = re.sub(illegal, '', s)
    return len(legal) / len(s)
