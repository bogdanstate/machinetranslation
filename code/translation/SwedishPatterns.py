import en

patterns = [
  lambda split:
    for i in range(0, len(split['translation'])):
      if split['swe_pos'][i] in ["NN","NP"]:
        if 'PLU' in split['features'][i]:
          split['translation'][i] = en.noun.plural(split['translation'][i]) 
        if 'DEF' in split['features'][i]:
          split['translation'][i] = "the %s" % split['translation'][i]
        if 'IND' in split['features'][i]:
          if split['original'][i] in ["en","ett"] and 
             split['translation'][i][0] in ['a','e','i','o','u'] and 
             split['translation'][i][0:1] != 'un':
            split['translation'][i-1] = "an"
          else:
            split['translation'][i-1] = "a"            
    return split
  
  lambda negate:
    # negate is (words,lemmas,tags,orderString,feats)
    # If negate words contain "inte":
    # if it follows a verb not equal to "vara" && "ha":
    #   exchange the position of "inte" and verb
    # return
    idx = len(negate[1]) - 1
    for i in reversed(range(1,len(negate[1]))):
      if negate[1][i].lower() == 'inte':
        if negate[1][i-1] == 'vara' or negate[1][i-1] == 'ha':
          continue
        if negate[2][i-1] == 'VB':
          for t in xrange(len(negate)):
            negate[t][i], negate[t][i-1] = negate[t][i-1], negate[t][i]
    return negate
]

for fn in patterns:
  split = fn(split)
