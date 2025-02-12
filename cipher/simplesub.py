import random
import cipher.cipher_utils as cipher_utils
import copy


######
# plain_alphabet: list sorted by decreasing frequency
def init_key(cipher_text, plain_alphabet):
    key=dict()
    cipher_alphabet=list(set(list(cipher_text)))
    random.shuffle(cipher_alphabet)
    unused=copy.deepcopy(plain_alphabet)
    for cipher_char in cipher_alphabet:
      if len(unused)>0:
        plain_char=cipher_utils.frequency_choice(unused)
        unused.remove(plain_char)
      else:
        # repeated plain characters, if cipher_alphabet is too large
        plain_char=cipher_utils.frequency_choice(plain_alphabet)
      key[cipher_char]=plain_char
    return cipher_utils.sort_dict(key)

######
# change a single plain character
def change_key(key, cipher_text, plain_alphabet):
    switch = True
    klist=list(key.keys())
    cipher_alphabet=sorted(list(set(list(cipher_text))))
    
    # plain_alphabet larger than cipher_alphabet?
    #diff=set(plain_alphabet)-set(key.values())
    diff=copy.deepcopy(plain_alphabet)
    for k in set(key.values()):
      diff.remove(k)

    # .2 -> QUAD_SCORE: -57.90462 TOT_SCORE: -61.79455 
    # .3 -> QUAD_SCORE: -54.28803 TOT_SCORE: -47.65132
    # .4 -> QUAD_SCORE: -58.93601 TOT_SCORE: -68.24649 
    # .5 -> QUAD_SCORE: -67.61419 TOT_SCORE: -54.91635
    if len(diff)>0 and random.random()>.5 : #pick unused plain character
      key[random.choice(klist)]=cipher_utils.frequency_choice(diff)
    else: #swap two values
      k1=random.choice(klist)
      k2=random.choice(klist)
      while k2==k1 or key[k2]==key[k1]:
        k2=random.choice(klist)
      temp=key[k1]
      key[k1]=key[k2]
      key[k2]=temp

    return cipher_utils.sort_dict(key)
    
def score(quad_score, plain_text):
  return quad_score

