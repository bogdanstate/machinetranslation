from SentenceSplitter import SentenceSplitter
import pickle, csv

dict_file = open('../../dictionaries/dictionary.pkl', 'rb')
lang_dict = pickle.load(dict_file)

class Baseline:
  def get_translation(self, word, pos):
    word = word.lower()
    pos = pos.lower()
    if (word, pos) in lang_dict:
      return lang_dict[(word,pos)][0]
    if (word, '') in lang_dict:
      return lang_dict[(word,'')][0]
    return word

  def translateCorpora(self, fconll):
    ss = SentenceSplitter()
    s = list(csv.reader(open(fconll, 'rb'), delimiter='\t'))
    sents = ss.split_sentence(s)
    for sent in sents:
      t = []
      for w in xrange(len(sent[0])):
        t.append(self.get_translation(sent[0][w], sent[1][w]))
      print self.formatSent(t) + '\n'

  def formatSent(self, slist):
    sent = " ".join(slist)
    sent = sent[:1].upper() + sent[1:]
    sent = sent.replace(' ,',',')
    sent = sent.replace(' .','.')
    sent = sent.replace(' !','!')
    sent = sent.replace(' :',':')
    sent = sent.replace(' /','/')
    sent = sent.replace('( ','(')
    sent = sent.replace(' )',')')
    return sent

trans = Baseline()
trans.translateCorpora('../../input_data/test_set_sv.conll')