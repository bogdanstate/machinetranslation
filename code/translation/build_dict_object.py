import pickle
from StochasticDictionary import StochasticDictionary

DICT_FILE = "../../dictionaries/corpora_dict.txt"

swe_dict_file = open('../../dictionaries/dictionary.pkl', 'wb')
d = StochasticDictionary()
d.build_from_dict_file(DICT_FILE)
pickle.dump(d, swe_dict_file)
swe_dict_file.close()

#swe_eng_dict =  collections.defaultdict(empty_defaultdict) 
#eng_swe_dict =  collections.defaultdict(empty_defaultdict) 

#pickle.dump(eng_swe_dict, eng_dict_file)
#eng_dict_file = open('../../dictionaries/rev_dictionary.pkl', 'wb')

#eng_dict_file.close()

