"""Rules for negation (eg. inte)"""

class NegationHandler:
	def reorderNeg(self,sentObj):
		# sentObj is (words,lemmas,tags,orderString,feats)
		# If sentObj words contain "inte":
		#	if it follows a verb not equal to "vara":
		#		exchange the position of "inte" and verb
		# return 
		


	def translateNeg(self,sentObj):
		# "not", "do not", "does not"