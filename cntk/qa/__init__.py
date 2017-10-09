#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
from cntk.qa.qa_processor import QuestionProcessor, AnswerProcessor

__all__ = ['QuestionProcessor', 'AnswerProcessor']

question_processor = QuestionProcessor()
answer_processor = AnswerProcessor()
