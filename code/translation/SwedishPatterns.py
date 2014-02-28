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
]

for fn in patterns:
  split = fn(split)
