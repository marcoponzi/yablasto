import random
import cipher.cipher_utils as cipher_utils
import copy
import math

    
def init_key(cipher_text, plain_alphabet):
    key=dict()
    cipher_alphabet=sorted(list(set(list(cipher_text))))
    alpha=copy.deepcopy(cipher_alphabet)
    random.shuffle(alpha)
    unused=copy.deepcopy(plain_alphabet)
    
    n_nulls=random.randint(1,int(len(cipher_alphabet)/3))

    for cipher_char in alpha:
      #if len(unused)==0 or random.random()<.2:
      if list(key.values()).count('_')<n_nulls: # exactly 3 nulls
        plain_char='_'
      else:
        plain_char=random.choice(unused)
        unused.remove(plain_char)
      key[cipher_char]=plain_char
    return cipher_utils.sort_dict(key)

######
# change a single plain character
def change_key(key, cipher_text, plain_alphabet):
    switch = True
    klist=list(key.keys())
    
    diff=set(plain_alphabet)-set(key.values())
    
    if len(diff)>0 and random.random()<.07: # replace with unused plain character
      #print("CHANGE")
      k=random.choice(klist)
      key[k]=random.choice(list(diff))
    elif list(key.values()).count('_')<len(key)/3 and random.random()<0.01: # add null
      k=random.choice(list(cipher_text))
      while key[k]=='_':
        k=random.choice(list(cipher_text))
      key[k]='_'
    else: #swap two values
      k1=random.choice(list(cipher_text))
      count=0
      k2=random.choice(klist)
      while k2==k1 or key[k2]==key[k1]:
        k2=random.choice(klist)
      temp=key[k1]
      key[k1]=key[k2]
      key[k2]=temp

    return cipher_utils.sort_dict(key)
    
def score(quad_score, plain_text):
  # favor solutions resulting in longer text and more varied alphabet (fewer nulls)
  return quad_score/(5+float(len(plain_text))/20.0+math.pow(len(set(plain_text)),1))

