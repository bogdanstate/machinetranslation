# -*- coding: utf-8 -*-
import re, codecs, operator, sys, collections

"""This file helps normalize translation score based on
   input file in which each line is in the format of 
   'sv,en\tscore' 
   A normalized score file is generated.
"""
class NormTransScore:
    def __init__(self):
        self.count = collections.defaultdict(lambda: collections.defaultdict(float))
        self.en_sum = collections.defaultdict(float)
        self.sv_sum = collections.defaultdict(float)

    def writeNormScore(self,fin,fout):
        """Calcuate the normalized score and write to fout"""

        for line in fin:
            [sv, en, score] = re.split(r'\t|,',line)
            self.count[sv][en] += float(score)
            self.en_sum[en] += float(score)
            self.sv_sum[sv] += float(score)

        for sv, ens in self.count.iteritems():
            for en in ens.keys():
                fout.write(sv + "," + en + "\t" + str(self.count[sv][en] / self.sv_sum[sv] * self.en_sum[en]) + "\n")                 

    def loadNormScoreFile(self,file):
        self.fname = file

    def getTransScores(self,query):
        query = query.decode('utf-8')
        f = codecs.open(self.fname, 'r', 'utf-8')
        answers = {}
        for line in f:
            [sv, en, score] = re.split(r'\t|,',line)
            if sv == query:
                answers[en] = float(score)
        return sorted(answers.iteritems(), key=operator.itemgetter(1), reverse=True)

"""
Main program for testing
"""
if __name__ == "__main__":
    nts = NormTransScore()
    nts.writeNormScore(sys.stdin.readlines(), sys.stdout)
