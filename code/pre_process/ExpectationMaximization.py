# -*- coding: utf-8 -*-
"""IBM Model I (with special NULL alignment) to calculate Trans_Prob(sv|en)"""
"""Ref1:https://facwiki.cs.byu.edu/cs479/index.php/Project_5_Tutorial"""
"""Ref2:http://www.cs.jhu.edu/~alopez/papers/model1-note.pdf"""

import math,sys,operator

def loadCorpora(file_name):
  """Loads text files as lists of lines. Used in evaluation."""
  svs = []
  ens = []
  o = open('sents.svs','w')
  with open(file_name) as f:
      for sv_line,en_line in zip(f,f):
        svs.append(sv_line)
        ens.append(en_line)
        o.write(sv_line)
  return (svs, ens)

def loadList(file_name):
  """Loads text files as lists of lines. Used in evaluation."""
  with open(file_name) as f:
      l = [f.next() for x in xrange(10)]
  return l

class ExpectationMaximization:
  def __init__(self, svs, ens):
    self.pnull = 0.2
    self.observes = []  # (sv, en)
    self.svVocab = []
    self.enVocab = []
    self.transProb = {}  # t(sv|en)
    self.getObserves(svs,ens)
    self.initProbs()

  def initProbs(self):
    """Initiate p(sv|en) uniformly"""
    for sent_pair in self.observes:
      for sv in sent_pair[0]:
        if sv not in self.svVocab:
          self.svVocab.append(sv)
      for en in sent_pair[1]:
        if en not in self.enVocab:
          self.enVocab.append(en)

    initProb = (1.0 - self.pnull)/len(self.svVocab)
    initNullProb = self.pnull/len(self.svVocab)
    self.transProb['NULL'] = {}
    for sv in self.svVocab:
      self.transProb['NULL'][sv] = initNullProb
      for en in self.enVocab:
        if en not in self.transProb:
          self.transProb[en] = {}
        if sv not in self.transProb[en]:
          self.transProb[en][sv] = initProb
          
  def getObserves(self, svs, ens):
    """Load non-punctuation sentence pairs"""
    """We can get non-punctuation files by pre-process/remove_punc.sh"""
    for i in range(len(svs)):
      pair = (svs[i].split(),ens[i].split())
      self.observes.append(pair)

    # Test samples:
    # self.observes = [(['casa','verde'],['green','house']),\
    #                  (['la','casa'],['the','house'])]
    # self.observes = [(['çocuklar','söylerim'],['children','sing']),\
    #                  (['melodileri','söylerim'],['sing','melodies']),\
    #                  (['mutlu','çocuklar'],['happy','children'])]

  def train(self,maxloop=100):
    initTransCount = {}
    initTransCount['NULL'] = {}
    for sv in self.svVocab:
      initTransCount['NULL'][sv] = 0
      for en in self.enVocab:
        if en not in initTransCount:
          initTransCount[en] = {}
        if sv not in initTransCount[en]:
          initTransCount[en][sv] = 0

    iter = 0
    logLikelihood = sys.maxint

    while iter < maxloop:
      iter += 1

      """Initiate transCount to all 0s"""
      transCount = initTransCount

      """E Step"""
      for sent_pair in self.observes:
        enLen = len(sent_pair[1])
        for sv in sent_pair[0]:
          s = 0
          for en in sent_pair[1]:
            s += self.transProb[en][sv]
          s = s*(1-self.pnull)/enLen
          denom = (self.pnull*self.transProb['NULL'][sv]+s)

          '''NULL word case'''
          p = self.pnull*self.transProb['NULL'][sv]/denom
          if sv not in transCount['NULL']:
            transCount['NULL'][sv] = 0
          transCount['NULL'][sv] += p

          '''Regular word case'''
          for en in sent_pair[1]:
            p = ((1-self.pnull)/enLen*self.transProb[en][sv])/denom
            transCount[en][sv] += p

      """M Step"""
      for en in self.transProb:
        for sv in self.transProb[en]:
          self.transProb[en][sv] = transCount[en][sv]/sum(transCount[en].values())
    

    logTransProb = self.transProb
    """Get logarithemetic transProb"""
    for en in logTransProb:
        for sv in logTransProb[en]:
          if logTransProb[en][sv] > 0:
            logTransProb[en][sv] = math.log(logTransProb[en][sv])
          else:
            logTransProb[en][sv] = -float("inf")
    return logTransProb

"""
Main program for testing
"""
if __name__ == "__main__":
  # svs = loadList('../../corpora/europarl-nopunct-full.sv')
  # ens = loadList('../../corpora/europarl-nopunct-full.en')

  svs, ens = loadCorpora('../../corpora/corpora_nopunc.dev')

  em = ExpectationMaximization(svs,ens)
  transProb = em.train(2)
  
  print "Print Best Mappings: "
  for en in transProb:
    print en
    transProbSorted = sorted(transProb[en].iteritems(), key=operator.itemgetter(1),reverse=True)[:5]
    for tr in transProbSorted:
      print tr

