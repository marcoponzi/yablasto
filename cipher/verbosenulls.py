import random
import cipher.cipher_utils as cipher_utils
import cipher.verbosebigr as verbosebigr
import sys
import math
import string
import copy

# return a character or bigram
def rand_cipher_bit(key,cipher_text, plain_alphabet):
  return verbosebigr.rand_cipher_bit(key,cipher_text, plain_alphabet)


# TODO
def set_lexicon(lexicon, longest_word, lexicon_avg_len):
  return

######
''' create Initial key '''
def init_key(cipher_text, plain_alphabet):
    key=dict()
    characters=copy.deepcopy(plain_alphabet)
    for i in range(0,random.randint(1,int(len(plain_alphabet)/4))):
      characters.append('_')
    for char in characters:
      cipher_bit=rand_cipher_bit(key,cipher_text, plain_alphabet)
      key[cipher_bit]=char
    
    return cipher_utils.sort_dict(key)

######
''' swap 2 letters '''
def change_key(key, cipher_text, plain_alphabet):
  klist=list(key.keys())
  rand=random.random()
  if rand>.8: # add or remove key 960 950?: 52.1; 990 -51.8
        diff=list(set(plain_alphabet)-set(key.values()))
        if list(key.values()).count('_')<(len(plain_alphabet)/4) and random.random()>.5:
          diff=diff+['_']       
        #if len(diff)>0 and random.random()>pow(float(len(key))/float(len(plain_alphabet)),2): # 2: 52.1
        if len(diff)>0 and random.random()>.2: #.01:-49.8
          key[rand_cipher_bit(key,cipher_text, plain_alphabet)]=random.choice(diff)
        else:
          del key[random.choice(list(key.keys()))]
  elif rand>.3: #.07:-51.6
    switch = True
    while switch:
        i = random.choice(klist)
        j = random.choice(klist)
        temp = key[i]
        key[i] = key[j]
        key[j] = temp

        if key[i] != key[j]:
            switch=False
  else:
    k = random.choice(klist)
    temp=key[k]
    newkey=rand_cipher_bit(key,cipher_text, plain_alphabet)  
    while newkey==k:
      newkey=rand_cipher_bit(key,cipher_text, plain_alphabet)  
    del key[k]
    key[newkey]=temp

  return cipher_utils.sort_dict(key)
  
def score(quad_score, plain_text):
  # favor solutions resulting in longer text
  return quad_score/(math.pow(len(plain_text),0.1))

