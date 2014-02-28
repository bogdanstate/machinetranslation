# -*- coding: utf-8 -*-
from SentenceSplitter import SentenceSplitter
import pickle, csv, itertools, codecs
from BigramOracle import BigramOracle

dict_file = open('../../dictionaries/dictionary.pkl', 'rb')
lang_dict = pickle.load(dict_file)
bigram_oracle = open('../../dictionaries/bigrams.pkl', 'rb')
oracle_dict = pickle.load(bigram_oracle)
o = BigramOracle("../../dictionaries/bigrams.pkl","../../dictionaries/stem_dict.pkl")

class Translator:
	def __init__(self):
		pass
				
	def get_translations(self, word, pos, lang_dict):
		"""
		Outputs translation(s) of word if word in lang_dict,
		returns word as its own translation otherwise
		"""
		#print word, pos
		word = word.lower()
		pos = pos.lower()
		if (word, pos) in lang_dict:
			return lang_dict[(word,pos)]
		if (word, '') in lang_dict:
			return lang_dict[(word,'')]
		return [word]

	def generate_proposals(self, wordpos, lang_dict):
		"""
		Generates all proposals for the set of words provided, 
		based on information contained in lang_dict.
		"""
		proposed = [self.get_translations(word, pos, lang_dict) for (word, pos) in wordpos]
		all_bigrams = []
		for first_trans, next_trans in zip(proposed[:-1], proposed[1:]):
			bigrams = list(itertools.product(first_trans, next_trans))
			print bigrams
			oracles_bigrams = o.show_me_the_path(bigrams, 1)
			if len(oracles_bigrams) == 0:
			    oracles_bigrams = bigrams
			all_bigrams += oracles_bigrams

	def translateCorpora(self, fconll):
		ss = SentenceSplitter()
		s = list(csv.reader(open(fconll, 'rb'), delimiter='\t'))
		sents = ss.split_sentence(s)
		i = 0
		
		for sent in sents:
			i += 1
			out = codecs.open('../../output_data/dev_set_trans_' + str(i), 'w')
			proposals = self.generate_proposals(zip(sent[0],sent[2]), lang_dict)
			# for item in proposals:
			# 	st = sent[3] % item
			# 	out.write(st)
		 #  		out.write('\n')
		  		#print st
		  		#print '\n'

	# def isRare(self, s):
	# 	s_list = s.split()
	# 	candidates = zip(s_list[:-1], s_list[1:])
	# 	oracle_says = o.show_me_the_path(candidates, ):
	# 		if oracle_dict[(a, b) == 0:
	# 			print a, b
	# 			return False

trans = Translator()
trans.translateCorpora('../../input_data/dev_set_sv.conll')