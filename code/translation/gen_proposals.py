# -*- coding: utf-8 -*-
import re
import itertools
import pickle
import codecs
import sys
from SentenceSplitter import SentenceSplitter

lang_dict = {
	u'han':['he'],
	u'sade':['said'],
	u'jag':['I'], 
	u'är':['are','is','am'], 
	u'inte':['not'], 
	u'rädd':['afraid','fearful']
	}
pkl_file = open('../../dictionaries/dictionary.pkl', 'rb')
lang_dict = pickle.load(pkl_file)

sentences = [u"Han sade, jag är inte rädd.", u"Oh vad stora ögon du har! sa Rödluvan"]

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


def get_translations(word, lang_dict):
  """
  Outputs translation(s) of word if word in lang_dict,
  returns word as its own translation otherwise
  """
  if word in lang_dict:
    return lang_dict[word]
  return [word]

def generate_proposals(words, lang_dict):
  """
  Generates all proposals for the set of words provided, 
  based on information contained in lang_dict.
  """
  return itertools.product(*[get_translations(word, lang_dict) for word in words])

for sentence in sentences:
  print "The sentence is"
  print sentence
  print "We split the sentence into its constituent words:"
  splitter = SentenceSplitter()
  [words, order] = splitter.split_sentence(sentence)
  print words
  print "...and a C-style formatting string."
  print order
  print "We generate the following proposals:"
  proposals = generate_proposals(words, lang_dict)
  for item in proposals:
    print order % item
  print "\n"
