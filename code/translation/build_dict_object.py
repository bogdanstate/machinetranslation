import pickle
import collections

DICT_FILE = "../../dictionaries/corpora_dict.txt"

swe_dict_file = open('../../dictionaries/dictionary.pkl', 'wb')

swe_eng_dict =  collections.defaultdict(list) 
eng_swe_dict =  collections.defaultdict(list) 

for line in open(DICT_FILE,'r').readlines():
  try: 
    [swe, eng_words, pos] = line.strip().split('\t',2)
  except:
    [swe, eng_words] = line.strip().split('\t',1)
  eng_words = eng_words.split('#')
  print eng_words
  if pos:
    swe_eng_dict[(swe, pos)] += eng_words
  swe_eng_dict[(swe, "")] += eng_words

pickle.dump(swe_eng_dict, swe_dict_file)
swe_dict_file.close()

#eng_dict_file = open('../../dictionaries/rev_dictionary.pkl', 'wb')

#eng_dict_file.close()

