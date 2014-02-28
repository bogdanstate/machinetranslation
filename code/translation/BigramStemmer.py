import sys, nltk
import collections
import pickle
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
counter = collections.defaultdict(collections.Counter)

lines = open("../../dictionaries/corpora_dict.txt").readlines()
stems = [l.split('\t')[1].replace('\n','').replace(' ','#').split('#') for l in lines]
stems = sum(stems, []) 
stems = [stemmer.stem(s) for s in stems]

for line in sys.stdin:
  line = line.strip().replace(","," ").replace('.'," ").split(' ')
  line = [stemmer.stem(x) for x in line]
  line = [x.lower() for x in line]
  for item in zip(line[:-1],line[1:]):
    if item[0]!='' and item[1] != '' and item[0] in stems and item[1] in stems: 
      print "%s\t%s" % item
