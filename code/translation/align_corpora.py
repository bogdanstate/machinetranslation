import collections
# work-around due to inability to pickle lambdas
def empty_defaultdict():
  return collections.defaultdict(list)

import sys
from Aligner import Aligner
from SentenceSplitter import SentenceSplitter
import pickle
import codecs



#UTF8Writer = codecs.getwriter('utf8')
#sys.stdout = UTF8Writer(sys.stdout)
char_stream = codecs.getreader("utf-8")(sys.stdin)
#UTF8Reader = codecs.getreader('utf8')
#sys.stdin = UTF8Reader(sys.stdin)

pkl_file = open('../../dictionaries/dictionary.pkl', 'rb')
lang_dict = pickle.load(pkl_file)
pkl_file.close()
pkl_file = open('../../dictionaries/rev_dictionary.pkl', 'rb')
rev_lang_dict = pickle.load(pkl_file)
pkl_file.close()
aligner = Aligner(lang_dict, rev_lang_dict)
splitter = SentenceSplitter()

for line in char_stream:
  try:
    [sentence, translation] = line.strip().split('\t')
    [sentence, dummy] = splitter.split_sentence(sentence)
    [translation, dummy] = splitter.split_english_sentence(translation)
    aligner.print_dict_alignments(sentence, translation, 5)
  except ValueError:
    pass
