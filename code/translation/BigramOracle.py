import pickle
import sys
import collections


class BigramOracle:
  def __init__(self, path, stem_dict_path):
    bigrams_file = open(path, 'rb')
    self.d = pickle.load(bigrams_file)
    bigrams_file.close()
    stem_dict_file = open(stem_dict_path, 'rb')
    self.stem_dict = pickle.load(stem_dict_file)
    stem_dict_file.close()
  def show_me_the_path(self, candidates, num_desired):
    c = collections.Counter() 
    punct_marks = [".",",","-",";",":"]
    punct = [ x for x in candidates if x[0] in punct_marks or x[1] in punct_marks]
    not_punct = [ x for x in candidates if x[0] not in punct_marks and x[1] not in punct_marks]
    for first, second in not_punct:
      first_stem = self.stem_dict[first.lower().split(' ')[-1]]
      second_stem = self.stem_dict[second.lower().split(' ')[0]]
      c[(first, second)] = self.d[first_stem][second_stem]
    return [x[0] for x in c.most_common(num_desired) if x[1] > 0] + punct

if __name__ == "__main__":
  o = BigramOracle("../../dictionaries/bigrams.pkl","../../dictionaries/stem_dict.pkl")
  candidates = [("blerjrhka such","that fdkajfld"), ("as", "if"), ("into","wife"), ("year","at"), ("year", "in")]
  print o.show_me_the_path(candidates, 3)
