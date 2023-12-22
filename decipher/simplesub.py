import random
import decipher.decipher_utils as decipher_utils
import copy


######
def init_key(cipher_text, plain_alphabet):
    key=dict()
    cipher_alphabet=sorted(list(set(list(cipher_text))))
    unused=copy.deepcopy(plain_alphabet)
    for cipher_char in cipher_alphabet:
      if len(unused)>0:
        plain_char=random.choice(unused)
        unused.remove(plain_char)
      else:
        # repeated plain characters, if cipher_alphabet is too large
        plain_char=random.choice(plain_alphabet)
      key[cipher_char]=plain_char
    return decipher_utils.sort_dict(key)

######
# change a single plain character
def change_key(key, cipher_text, plain_alphabet):
    switch = True
    klist=list(key.keys())
    cipher_alphabet=sorted(list(set(list(cipher_text))))
    
    diff=set(plain_alphabet)-set(key.values())
    
    if len(diff)>0 and random.random()>.2: #pick unused plain character
      key[random.choice(klist)]=random.choice(list(diff))
    else: #swap two values
      k1=random.choice(klist)
      k2=random.choice(klist)
      while key[k2]==key[k1]:
        k2=random.choice(klist)
      temp=key[k1]
      key[k1]=key[k2]
      key[k2]=temp

    return decipher_utils.sort_dict(key)

