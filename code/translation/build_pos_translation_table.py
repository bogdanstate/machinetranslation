import csv
import pickle
import codecs
import math
from collections import Counter
from collections import defaultdict
lookup = defaultdict(Counter)

from SentenceSplitter import SentenceSplitter
from StochasticDictionary import StochasticDictionary


pkl_file = open('../../dictionaries/dictionary.pkl', 'rb')
d = pickle.load(pkl_file)
pkl_file.close()
ss = SentenceSplitter()

engTreeTagged = '../../input_data/dev_set_en_tagged.txt'
e = list(csv.reader(open(engTreeTagged, 'rb'), delimiter='\t'))
esplit = ss.split_english_sentence(e)

sweconll = '../../input_data/dev_set_sv.conll'
char_stream = codecs.getreader("utf-8")(open(sweconll, 'rb'))
s = [x.replace('\n','').split('\t') for x in char_stream.readlines()]
ssplit = ss.split_sentence(s)

for sent in zip(ssplit, esplit):
  ssent = sent[0]
  esent = sent[1]
  for (lemma, tag) in zip(ssent[0], ssent[1]):
    trans = d.get_translations(lemma, tag.lower()) 
    if trans == []:
      trans = d.get_translations(lemma, "")
    trans = [x[0] for x in trans if len(x[0].split(" ")) == 1]
    eng_tags = [eng_tag[0:2] for lemma, eng_tag in zip(esent[0], esent[1]) if lemma in trans]
    for eng_tag in eng_tags:
      lookup[tag][eng_tag] += 1

pos = {}
for swe_tag, v in lookup.iteritems():
  num_types = len(v.keys())
  total = math.log(sum(v.values()) + num_types)
  pos[swe_tag] = {}
  for eng_tag, count in v.iteritems():
    pos[swe_tag][eng_tag] = math.log(count + 1) - total

print pos

pos_file = open('../../dictionaries/pos.pkl', 'wb')
pickle.dump(pos, pos_file)
pos_file.close()

