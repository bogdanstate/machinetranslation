# -*- coding: utf-8 -*-
import itertools
import collections
import pickle
import codecs
import sys
from SentenceSplitter import SentenceSplitter

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# work-around due to inability to pickle lambdas
def empty_defaultdict():
  return collections.defaultdict(list)

class Aligner:
  def __init__(self, dictionary, rev_dictionary):
    self.lang_dict = dictionary
    self.rev_dict = rev_dictionary
  def align_all_pairs(self, first, second):
    """
    Aligns all pairs between the first and second list.
    """
    alignments = itertools.product(first, second)
    return alignments
  def compound_noun_search(self, word, translations):
    """
    If a word can be written as a composition of its proposed translations
    reverse-translations (e.g. Europaparlament, European=Europa Parliament=Parlament),
    return the composition as a translation.
    """
    rev_translations = [(t, self.rev_dict[t]) for t in translations]
    potential_translations = [x for x in zip(rev_translations[:-1], rev_translations[1:])]
    for proposal in potential_translations:
      if len(proposal[0][1][0]) > 0 and len(proposal[1][1][0]) > 0:
        proposed_words = ["%s%s" % x for x in itertools.product(proposal[0][1][0], proposal[1][1][0])]
        if word in proposed_words:
          translation_index = [i for i in range(0, len(translations)) if translations[i] == proposal[0][0] or translations[i] == proposal[1][0]]
          found_translation = "%s_%s" % (proposal[0][0], proposal[1][0])
          return (translation_index, found_translation) 
    return ([], [])
    
  def dict_search(self, word, translations):
    """
    If a word *as well as* its proposed translations are in the
    provided dictionary, then return the pair. Else,
    return an empty list.
    """
    matches = [self.lang_dict[word][pos] for pos in self.lang_dict[word]]
    matches = sum(matches, [])
    matches = list(set(translations).intersection(set(matches)))
    if len(matches) > 0:
      return matches
    if word[-2:] == "et" or word[-2:] == "en":
      art_trans = [x for x in translations if x[:4] == "the_"]  
      matches = list(set(art_trans).intersection(set(["the_%s" % x for x in self.lang_dict[word[:-2]]])))
      return matches
    return []

  def align_with_dict(self, first, second, k):
    """
    Search for matches between a word's potential translations
    in the dictionary. If found then consider only those matches
    as candidates for alignments. Else consider all the unmatched
    translations in a -k:k window as candidates.
    """
    dict_matches = [self.dict_search(word, second) for word in first]
    print dict_matches
    #matched_trans = sum(dict_matches, [])
    #unmatched_trans_index = [i for i in range(0, len(second)) if second[i] not in matched_trans]
    #unmatched_index = [i for i in range(0, len(dict_matches)) if len(dict_matches[i]) == 0]
    # search for compound words
    #for i in unmatched_index:
    #  potential_match_index = [j for j in unmatched_trans_index if j >= i - k and j <= i + k]
    #  [index, translation] = self.compound_noun_search(first[i], [second[j] for j in potential_match_index])
    #  if len(index) > 0:
    #    dict_matches[i] = [translation]
    #    unmatched_trans_index = [unmatched_trans_index[i] for i in range(0, len(unmatched_trans_index)) if i not in index]
    # output all other alignments
    #unmatched_index = [i for i in range(0, len(dict_matches)) if len(dict_matches[i]) == 0]   
    #for i in unmatched_index:
    #  dict_matches[i] = [second[j] for j in unmatched_trans_index if j >= i - k and j <= i + k]
    #alignments = [[ 
    #                 (x[0],x[1][0],1.0/len(matches)) 
    #                 for x in itertools.product([word], matches)
    #                 ] 
    #               for word, matches in 
    #                 zip(first, dict_matches)
    #             ]
    #return alignments

  def print_dict_alignments(self, sentence, translation, k):
    """
    Prints a series of alignments.
    """
    #for proposals in 
    d = self.align_with_dict(sentence, translation, k)
    #:
      #for alignment in proposals:
        #print "%s,%s\t%0.4f" % alignment

s_1 = u"ministeren har språkit på Europaparlament."
s_2 = u"The minister has spoken at Europe Parliament."
pkl_file = open('../../dictionaries/dictionary.pkl', 'rb')
lang_dict = pickle.load(pkl_file)
pkl_file.close()
pkl_file = open('../../dictionaries/rev_dictionary.pkl', 'rb')
rev_lang_dict = pickle.load(pkl_file)
pkl_file.close()
aligner = Aligner(lang_dict, rev_lang_dict)
splitter = SentenceSplitter()

[s_1, dummy] = splitter.split_sentence(s_1)
[s_2, dummy] = splitter.split_english_sentence(s_2)
aligner.print_dict_alignments(s_1, s_2, 3)
