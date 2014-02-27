# -*- coding: utf-8 -*-
''' This file generates a Swedish to English dictionary based on 
    folkets_sv_en_public.xml.
    The format of each entry is 
      Swedish (\t) English#English  (\t)  Word Class '''

import xml.etree.ElementTree as ET

dictionary = ET.parse('../../dictionaries/folkets_sv_en_public.xml')
root = dictionary.getroot()

f = open('../../dictionaries/dictionary.txt','w')

for entry in root.findall('word'):
  value = entry.get('value')
  translations = entry.findall('translation')
  klass = entry.get('class')
  pars = entry.findall('paradigm')

  if klass is None:
    klass = ''
  f.write(entry.get('value').encode('UTF-8') + '\t')
  f.write('#'.join([t.get('value').encode('UTF-8') for t in translations]))
  f.write('\t' + klass + '\n')

  for p in pars:
    infs = p.findall('inflection')
    for inf in infs:
      f.write(inf.get('value').encode('UTF-8') + '\t')
      f.write('#'.join([t.get('value').encode('UTF-8') for t in translations]))
      f.write('\t' + klass + '\n')

f.close()
