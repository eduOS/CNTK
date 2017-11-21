# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from __future__ import absolute_import
from __future__ import division
from collections import OrderedDict


def build_vocabulary(mode, inpath_regex, outpath_regex,
                     match_regex=None, unmatch_regex=None, default=None):
    """
    args:
        mode: "word" or "char"

    """
    word_freqs = OrderedDict()
    worddict = OrderedDict()
    if mode == "word":
        worddict['<s>'] = sys.maxint
        worddict['</s>'] = sys.maxint
        worddict['[PAD]'] = sys.maxint
        worddict['[UNK]'] = sys.maxint
        worddict['[STOP]'] = sys.maxint
        worddict['[START]'] = sys.maxint

    assert len(sys.argv) > 3, "numbers of args must be more then 4"
    for filename in sys.argv[2:-1]:
        print('Processing', filename)
        with open(filename, 'r', 'utf-8') as f:
            for line in f:
                if line.strip().startswith("<"):
                    continue
                line = standardizor.set_sentence(line).standardize('all').digits().sentence
                if mode == "word":
                    words_in = tokenizer.sentence2words(line, punc=False)
                elif mode == "char":
                    words_in = text2charlist(line)
                for w in words_in:
                    if w not in word_freqs:
                        word_freqs[w] = 0
                    word_freqs[w] += 1

    words = word_freqs.keys()
    freqs = word_freqs.values()
    # print freqs
    # ipdb.set_trace()
    sorted_idx = numpy.argsort(freqs)
    # print sorted_idx
    sorted_words = [words[ii] for ii in sorted_idx[::-1]]

    with open('%s' % sys.argv[-1], 'w', 'utf-8') as f:
        for ii, ww in enumerate(sorted_words):
            worddict[ww] = ii
            f.write(ww + " " + str(ii) + "\n")

    print('Done')
