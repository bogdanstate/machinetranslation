import en

class NodeBoxMorphs:
	def __init__(self):
		self.vb = en.verb
		self.nn = en.noun
	
	"""Get morphs of a verb"""
	def getPresentForms(self,verb):
		forms = []
		for p in [1,2,3]:
			w = self.vb.present(verb, person=p)
			if w not in forms:
				forms.append(w)
		return forms
	
	def getPresentParticipleForms(self,verb):
		return [self.vb.present_participle(verb)]
	
	def getPastForms(self,verb):
		forms = []
		for p in [1,2,3]:
			w = self.vb.past(verb, person=p)
			if w not in forms:
				forms.append(w)
		return forms
	
	def getPastParticipleForms(self,verb):
		return [self.vb.past_participle(verb)]

	def getVerbForms(self,verb):
		prf = self.getPresentForms(verb)
		prpf = self.getPresentParticipleForms(verb)
		paf = self.getPastForms(verb)
		papf = self.getPastParticipleForms(verb)
		return list(set(prf + prpf + paf + papf))

	"""Get morphs of a noun"""
	def getPlural(self,noun):
		return self.nn.plural(noun)

	def getSingular(self,noun):
		return self.nn.singular(noun)


if __name__ == "__main__":
	nbm = NodeBoxMorphs()
	print nbm.getPastForms('run')
	print nbm.getSingular('children')




