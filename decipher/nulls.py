import random
import decipher.decipher_utils as decipher_utils
import copy


    
def init_key(cipher_text, plain_alphabet):
    key=dict()
    cipher_alphabet=sorted(list(set(list(cipher_text))))
    unused=copy.deepcopy(plain_alphabet)

    for cipher_char in cipher_alphabet:
      if len(unused)==0 or random.random()<.2:
        plain_char='_'
      else:
        plain_char=random.choice(unused)
        unused.remove(plain_char)
      key[cipher_char]=plain_char
    return decipher_utils.sort_dict(key)

######
# change a single plain character
def change_key(key, cipher_text, plain_alphabet):
    switch = True
    klist=list(key.keys())
    cipher_alphabet=sorted(list(set(list(cipher_text))))
    
    diff=set(plain_alphabet)-set(key.values())
    
    if len(diff)>0 and random.random()<.2: #pick unused plain character 0.2 -98
      key[random.choice(klist)]=random.choice(list(diff))
    elif list(key.values()).count('_')<len(key)/2 and random.random()<.03: # add a new null 0.03 -98
      k=random.choice(klist)
      while key[k]=='_':
        k=random.choice(klist)
      key[k]='_'
    else: #swap two values
      k1=random.choice(klist)
      k2=random.choice(klist)
      while key[k2]==key[k1]:
        k2=random.choice(klist)
      temp=key[k1]
      key[k1]=key[k2]
      key[k2]=temp

    return decipher_utils.sort_dict(key)

