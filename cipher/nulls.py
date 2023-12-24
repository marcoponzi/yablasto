import random
import cipher.cipher_utils as cipher_utils
import copy


    
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
    
    if len(diff)>0 and random.random()<.01: # replace with unused plain character
      #print("CHANGE")
      k=random.choice(klist)
      #count=0
      #while key[k]=='_': # and count<3: # preference for replacing nulls
      #  k=random.choice(klist)
      #count+=1
      key[k]=random.choice(list(diff))
    elif list(key.values()).count('_')<len(key)/3 and random.random()<0.01: # add null
      k=random.choice(list(cipher_text))
      while key[k]=='_':
        k=random.choice(list(cipher_text))
      key[k]='_'
    else: #swap two values
      k1=random.choice(list(cipher_text))
      count=0
      #if key[k1]!='_' and count<2: # try to swap a null and a non-null
      #  k1=random.choice(klist)
      #  count+=1
      k2=random.choice(klist)
      #if key[k2]!='_':
      #  k2=random.choice(klist)
      while k2==k1 or key[k2]==key[k1]:
        k2=random.choice(klist)
      temp=key[k1]
      key[k1]=key[k2]
      key[k2]=temp

    return cipher_utils.sort_dict(key)

