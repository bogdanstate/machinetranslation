# -*- coding: utf-8 -*-
import re
import csv

ALPHA_CHARS = "[a-zåäöïëéáóúí_-]+"
SPLIT_REGEX = re.compile(ALPHA_CHARS, re.IGNORECASE|re.UNICODE)
SPLIT_ENG_REGEX = re.compile("[a-z_-]+", re.IGNORECASE)
SWE_POS_TAGS = []
ENG_POS_TAGS = []

class SentenceSplitter:
  def split_sentence(self, f):
    """ 
    Read sentences from fconll and split each sentence into 
    a C-style formatting string and a list tuple of words.
    """
    split = []
    line = 0
    while line < len(f):
        words = []
        tags = []
        order = []
        while line < len(f) and f[line] and f[line][0] != u'':
            match = re.match(SPLIT_REGEX,f[line][2])
            if match:
                words.append(f[line][2])
                tags.append(f[line][3])
                order.append('%s')
                if f[line][3] not in SWE_POS_TAGS:
                    SWE_POS_TAGS.append(f[line][3])
            line += 1
        split.append((words,tags,order))
        line += 1
    return split

  def split_english_sentence(self, f):
    """ 
    Read sentences from Treetagged file and split each sentence into 
    a C-style formatting string and a list tuple of words.
    """
    split = []
    line = 0
    while line < len(f):
        words = []
        tags = []
        order = []
        while f[line] != ['<EOL>']:
            if re.match(SPLIT_ENG_REGEX,f[line][2]):
                words.append(f[line][2])
                tags.append(f[line][1])
                order.append('%s')
                if f[line][1] not in ENG_POS_TAGS:
                    ENG_POS_TAGS.append(f[line][1])
            line += 1
        split.append((words,tags,order))
        line += 1
    return split
    #sentence = re.sub("(?<=[^A-Za-z])the |^the ","the_", sentence.lower())

if __name__ == "__main__":
    ss = SentenceSplitter()
    sweconll = '../../input_data/dev_set_sv.conll'
    s = list(csv.reader(open(sweconll, 'rb'), delimiter='\t'))
    ssplit = ss.split_sentence(s)
    print ssplit[-1]

    engTreeTagged = '../../input_data/dev_set_en_tagged.txt'
    e = list(csv.reader(open(engTreeTagged, 'rb'), delimiter='\t'))
    esplit = ss.split_english_sentence(e)
    print esplit[-1]

    print SWE_POS_TAGS
    print ENG_POS_TAGS

