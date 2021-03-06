import csv
import pickle
import codecs
import math
from collections import Counter
from collections import defaultdict
lookup = defaultdict(Counter)

data = []
from SentenceSplitter import SentenceSplitter
from StochasticDictionary import StochasticDictionary


pkl_file = open('../../dictionaries/dictionary.pkl', 'rb')
d = pickle.load(pkl_file)
pkl_file.close()
ss = SentenceSplitter()

engTreeTagged = '../../input_data/eng_shuf_5000_tagged.txt'
e = list(csv.reader(open(engTreeTagged, 'rb'), delimiter='\t'))
esplit = ss.split_english_sentence(e)

sweconll = '../../input_data/swe_shuf_5000.conll'
char_stream = codecs.getreader("utf-8")(open(sweconll, 'rb'))
s = [x.replace('\n','').split('\t') for x in char_stream.readlines()]
ssplit = ss.split_sentence(s)

for sent in zip(ssplit, esplit):
  ssent = sent[0]
  esent = sent[1]
  for (word, lemma, swe_tag, feat) in zip(ssent[0], ssent[1], ssent[2], ssent[4]):
    trans = d[(lemma,swe_tag.lower())]
    #trans = [x[0] for x in trans if len(x[0].split(" ")) == 1]
    eng_tags = [en_tag for en_lemma, en_word, en_tag in zip(esent[0], esent[1], esent[2]) if en_lemma in trans]
    
    for eng_tag in eng_tags:
      lookup["|".join([swe_tag]+feat)][eng_tag] += 1
      data += [[eng_tag] + [swe_tag] + ["|".join(feat)]]

for line in data:
  print ",".join(line)

pos = {}
for swe_tag, v in lookup.iteritems():
  num_types = len(v.keys())
  total = math.log(sum(v.values()) + num_types)
  pos[swe_tag] = {}
  for eng_tag, count in v.iteritems():
    pos[swe_tag][eng_tag] = math.log(count + 1) - total


pos_file = open('../../dictionaries/pos.pkl', 'wb')
pickle.dump(pos, pos_file)
pos_file.close()

