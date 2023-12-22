import re


# key is a map: key:cipher-symbol, val:plain-text symbol
#  sorted by decreasing key length
def decrypt(cipher_text, key):
    plain=cipher_text
    for cipher_bit in key.keys():
      plain=re.sub(cipher_bit, key[cipher_bit],plain)
    plain = re.sub('_', '',plain) # remove nulls
    return plain
    
# longer keys first
def sort_dict(indict):
  new_d = {}
  klist=list(indict.keys())
  klist=sorted(klist) #alphabetical
  klist=sorted(klist, key=len, reverse=True) #longer first

  for k in klist:
    new_d[k] = indict[k]

  return new_d
