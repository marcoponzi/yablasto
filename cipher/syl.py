import random
import cipher.cipher_utils as cipher_utils
import copy
import math

# HOMOPHONIC (ONE TO MANY) CIPHER WHERE EACH CHARACTER IS ENCODED
# AS A SHORT WORD, ROUGHLY CORRESPONDING TO A SYLLABLE

######
def init_key(cipher_text, plain_alphabet):
    key=dict()
    cipher_alphabet=sorted(list(set(cipher_text.split('_'))))
    cipher_alphabet=[i for i in cipher_alphabet if i!= '']
    unused=copy.deepcopy(plain_alphabet)
    for cipher_char in cipher_alphabet:
      if len(unused)>0:
        plain_char=random.choice(unused)
        unused.remove(plain_char)
      else:
        # repeated plain characters, if cipher_alphabet is too large
        plain_char=random.choice(plain_alphabet)
      key[cipher_char]=plain_char
    return cipher_utils.sort_dict(key)

######
# change a single plain character
def change_key(key, cipher_text, plain_alphabet):
    switch = True
    klist=list(key.keys())
    cipher_alphabet=sorted(list(set(list(cipher_text))))
    
    diff=set(plain_alphabet)-set(key.values())
    
    if len(diff)>len(plain_alphabet)/3 or (len(diff)>0 and random.random()<.2): #pick unused plain character 9.18 .1
      key[random.choice(klist)]=random.choice(list(diff))
    else: 
      k1=random.choice(klist)
      k2=random.choice(klist)
      while key[k2]==key[k1]:
        k2=random.choice(klist)
      if random.random()<.1: # duplicate value
        key[k1]=key[k2] 
      else: #swap two values
        temp=key[k1]
        key[k1]=key[k2]
        key[k2]=temp

    return cipher_utils.sort_dict(key)
    
def score(quad_score, plain_text):
  # favor solutions that use more letters
  return quad_score/math.pow(len(set(plain_text)),0.5)

