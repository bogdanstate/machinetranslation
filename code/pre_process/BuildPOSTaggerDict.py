"""
Builds a POS-tagger dictionary object to query for translations
"""
import codecs

class PosTaggerDictionary:
	def __init__(self, dictText):
		self.dict = {}
		f = codecs.open(dictText, encoding='utf-8')
		for line in f:
		  entry = line.split('\t',2)
		  if len(entry) >= 3:
		  	[swe, eng, pos] = entry
		  	pos = pos.strip()
		  elif entry == 2:
		  	[swe, eng] = entry
		  	pos = None
		  elif entry == 1:
		  	swe = entry
		  	eng = None
		  	pos = None
		  if swe not in self.dict:
		  	self.dict[swe] = {}
		  if not pos:
		  	pos = 'NULL'
		  if pos not in self.dict[swe]:
		  	self.dict[swe][pos] = []
		  for token in eng.split('#'):
		  	if token not in self.dict[swe][pos]:
		  		self.dict[swe][pos].append(token)

	def getDict(self):
		return self.dict

	def getAllTrans(self,word):
		if word not in self.dict:
			return []
		trans = []
		for p in self.dict[word]:
			for t in self.dict[word][p]:
				trans.append(t)
		return trans

	def getPosTrans(self,word,pos):
		if word not in self.dict:
			return []
		trans = []
		if pos not in self.dict[word]:
			return []
		for t in self.dict[word][pos]:
			trans.append(t)
		return trans

if __name__ == "__main__":
	ptd = PosTaggerDictionary('../../dictionaries/corpora_dict.txt')
	sv_en_dict = ptd.getDict()
	print sv_en_dict['andra'].keys()
	print ptd.getPosTrans('andra','vb')
	print ptd.getAllTrans('andra')