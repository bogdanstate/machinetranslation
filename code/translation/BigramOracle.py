import pickle
import sys
import collections
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

class BigramOracle:
  def __init__(self, path):
    bigrams_file = open(path, 'rb')
    self.d = pickle.load(bigrams_file)
    bigrams_file.close()
  def show_me_the_path(self, candidates, num_desired):
    c = collections.Counter()
    for first, second in candidates:
      first_stem = stemmer.stem(first.lower().split(' ')[-1])
      second_stem = stemmer.stem(second.lower().split(' ')[0])
      c[(first, second)] = self.d[first_stem][second_stem]
    return [x for x in c.most_common(num_desired) if x[1] > 0]

if __name__ == "__main__":
  o = BigramOracle("../../dictionaries/bigrams.pkl")
  candidates = [("blerjrhka such","that fdkajfld"), ("green","witch"), ("your","mother"), ("European","Union"), ("as", "if")]
  print o.show_me_the_path(candidates, 3)
