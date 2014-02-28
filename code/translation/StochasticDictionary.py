"""
Builds a dictionary object from the original corpus dictioanry 
and serializes it to disk.

Dictionary format:
dict[(swe_lemma, swe_pos)][(eng_lemma, eng_pos)] = log_prob 

"""

import collections, codecs, math


class StochasticDictionary:
  def __init__(self):
    self.d = {}
    self.all_pos = set()

  def add_translation( self, swe_lemma, swe_pos, eng_lemma, eng_pos, log_prob ):
    """
    Add translation with Swedish lemma and POS tag and English lemma and POS tag.
    Use "" as dummy POS tags if needed.
    """
    swe_tag = (swe_lemma, swe_pos)
    eng_tag = (eng_lemma, eng_pos)
    self.all_pos.add( swe_pos )
    self.all_pos.add( eng_pos )
    if swe_tag in self.d:
      if eng_tag in self.d:
        # log-sum-exp trick
        old_log_prob = self.d[eng_tag][swe_tag]
        max_log_prob = max([old_log_prob, log_prob])
        new_log_prob = math.log( math.exp( old_log_prob - max_log_prob ) + 
                                 math.exp( log_prob - max_log_prob) ) + max_log_prob 
        self.d[swe_tag][eng_tag] = new_log_prob
      else:
        self.d[swe_tag][eng_tag] = log_prob
    else:
      self.d[swe_tag] = {}
      self.d[swe_tag][eng_tag] = log_prob
  
  def get_translations( self, swe_lemma, swe_pos ):
    """
    Return translation of a certain Swedish Lemma,
    as a list of the form (English lemma, english POS, log_prob)
    """
    if swe_pos == "":
      candidates = [ tag for tag in self.all_pos if (swe_lemma, tag) in self.d ]
      translations = []
      if len(candidates) > 0:
        norm_term = math.log(len(candidates))
        for tag in candidates: 
          translations += [(k[0], k[1], v - norm_term) for k, v in self.d[(swe_lemma, tag)].iteritems()]
      return translations
    swe_tag = (swe_lemma, swe_pos)
    if swe_tag not in self.d:
      return []
    translations = [(k[0], k[1], v) for k, v in self.d[(swe_lemma, swe_pos)].iteritems()]
    return translations 

  def build_from_dict_file(self, dict_file):
    """
    Construct Stochastic Dictionary from original dict file
    """
    f = codecs.open(dict_file, encoding='utf-8')
    for line in f.readlines():
      try:
        [swe, eng, swe_pos] = line.replace("\n","").split('\t', 2)
      except:
        [swe, eng] = line.replace("\n","").split('\t', 1)
        pos = ""
      swe_token = swe.replace("|","").lower()
      eng = eng.split('#')
      trans_log_prob = -math.log(len(eng))
      for eng_token in eng:
        self.add_translation(swe_token, swe_pos, eng_token, "", trans_log_prob)
    f.close()
 
  def print_dictionary(self):
    for swe_tag, v in self.d.iteritems():
      for eng_tag, prob in v.iteritems():
        print "%s,%s\t%s,%s\t%.4f" % (swe_tag[0], swe_tag[1], eng_tag[0], eng_tag[1], prob)
