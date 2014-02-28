"""Rules for negation (eg. inte)"""

class ReorderHandler:
	def reorderNeg(self,sentObj):
		# sentObj is (words,lemmas,tags,orderString,feats)
		# If sentObj words contain "inte":
		#	if it follows a verb not equal to "vara" && "ha":
		#		exchange the position of "inte" and verb
		# return
		idx = len(sentObj[1]) - 1
		for i in reversed(range(1,len(sentObj[1]))):
			if sentObj[1][i].lower() == 'inte':
				if sentObj[1][i-1] == 'vara' or sentObj[1][i-1] == 'ha':
					continue
				if sentObj[2][i-1] == 'VB':
					for t in xrange(len(sentObj)):
						sentObj[t][i], sentObj[t][i-1] = sentObj[t][i-1], sentObj[t][i]
					sentObj[0][i-1:i-1] = 'do'
					sentObj[1][i-1:i-1] = 'do'
					sentObj[2][i-1:i-1] = 'VB'
					sentObj[3][i-1:i-1] = '%s'
					sentObj[4][i-1:i-1] = ['_']
				
		return sentObj

	def reorderVerb(self,sentObj):
		idx = len(sentObj[1]) - 1
		verbFound = -1
		#print sentObj[1]
		for i in range(0,len(sentObj[1])):
			if sentObj[2][i] == 'NN' or sentObj[2][i] == 'PN' or sentObj[2][i] == 'PM' or sentObj[2][i] == 'PS':
				if verbFound >= 0:
					for t in xrange(len(sentObj)):
						elem = sentObj[t].pop(verbFound)
						sentObj[t].insert(i,elem)
				break
			if sentObj[2][i] == 'VB':
				verbFound = i
				
		return sentObj

	def process(self,sentObj):
		return self.reorderVerb(self.reorderNeg(sentObj))
		
if __name__ == "__main__":
	nh = ReorderHandler()
	print nh.process((['Visst', 'har', 'stora', 'framsteg', 'gjorts', 'inte', 'det', 'senaste', '\xc3\xa5ret', 'i', 'fr\xc3\xa5ga', 'om', 'utbildning', 'och'], ['visst', 'ha', 'stor', 'framsteg', 'g\xc3\xb6ra', 'inte', 'den', 'sen', '\xc3\xa5r', 'i', 'fr\xc3\xa5ga', 'om', 'utbildning', 'och'], ['AB', 'VB', 'JJ', 'NN', 'VB', 'PP', 'DT', 'JJ', 'NN', 'PP', 'NN', 'PP', 'NN', 'KN'], ['%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'], [['_'], ['PRS', 'AKT'], ['POS', 'UTR/NEU', 'PLU', 'IND/DEF', 'NOM'], ['NEU', 'PLU', 'IND', 'NOM'], ['SUP', 'SFO'], ['_'], ['NEU', 'SIN', 'DEF'], ['SUV', 'UTR/NEU', 'SIN/PLU', 'DEF', 'NOM'], ['NEU', 'SIN', 'DEF', 'NOM'], ['_'], ['UTR', 'SIN', 'IND', 'NOM'], ['_'], ['UTR', 'SIN', 'IND', 'NOM'], ['_']]))