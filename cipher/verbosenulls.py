import random
import cipher.cipher_utils as cipher_utils
import cipher.verbosebigr as verbosebigr
import sys
import math
import string
import copy
import re

my_lexicon=''
my_longest_word=''
my_lexicon_avg_len=''
my_cache=''

# return a character or bigram
def rand_cipher_bit(key,cipher_text, plain_alphabet):
  bigr_probability=.90 #.90 
  return verbosebigr.rand_cipher_bit(key,cipher_text, plain_alphabet,bigr_probability)


# TODO
def set_lexicon(lexicon, longest_word, lexicon_avg_len):
  global my_longest_word
  global my_lexicon
  global my_lexicon_avg_len
  global my_cache
  my_lexicon=lexicon
  my_longest_word=longest_word
  my_lexicon_avg_len=lexicon_avg_len
  my_cache=dict()

######
''' create Initial key '''
def init_key(cipher_text, plain_alphabet):
    key=dict()
    characters=copy.deepcopy(plain_alphabet)
    for i in range(0,random.randint(1,int(len(plain_alphabet)/4))):
      characters.append('_')
    for cipher_char in set(list(cipher_text)):
      if len(characters)>0:
        plain_char=random.choice(characters)
        characters.remove(plain_char)
      else:
        plain_char='_'
      key[cipher_char]=plain_char
    for char in characters:
      cipher_bit=verbosebigr.rand_cipher_bit(key,cipher_text, plain_alphabet,.2)
      key[cipher_bit]=char
    
    return cipher_utils.sort_dict(key)

######
def change_key(key, cipher_text, plain_alphabet): 
  key=copy.deepcopy(key)
  klist=list(key.keys())
  rand=random.random()
  diff=list(set(plain_alphabet)-set(key.values()))
  if rand>.90: # add or remove key .85 aaa **        
        nulls_bigr=list(key.values()).count('_')
        max_nulls_bigr=len(plain_alphabet)/3
        for k in list(key.keys()):
          if len(k)>1:
            nulls_bigr+=1
        if nulls_bigr<max_nulls_bigr and random.random()>.80: ### 90
          diff=diff+['_'] # possibly add a null
        ###print(str(len(diff))+" > "+str(len(plain_alphabet)/2))
        if nulls_bigr<max_nulls_bigr and len(diff)>0 and (len(diff)>len(plain_alphabet)/2 or random.random()>.50): # .50 ccc
          key[rand_cipher_bit(key,cipher_text, plain_alphabet)]=random.choice(diff)
        else:
          to_be_removed=random.choice(list(key.keys()))
          if len(to_be_removed)==1: #favour bigrams
            to_be_removed=random.choice(list(key.keys()))
          del key[to_be_removed]
  elif rand<.40: # 25 replace one key
    to_be_removed=random.choice(list(key.keys()))
    new_k=rand_cipher_bit(key,cipher_text, plain_alphabet)
    temp=key[to_be_removed]
    del key[to_be_removed]
    key[new_k]=temp
  else:
    # swap values for two keys, maybe altering one of the two
    i = random.choice(klist)
    j = random.choice(klist)
    count=0
    while key[i]==key[j] and count<999:
          j = random.choice(klist)
          count+=1
    temp = key[i]
    key[i] = key[j]
    if len(diff)==0 or random.random()>.40 : # 10 bbb
      key[j] = temp
    else:
      key[j] = random.choice(diff)
     
  return cipher_utils.sort_dict(key)
  
def change_key_delete(key, cipher_text, plain_alphabet):
  #print("**** "+cipher_utils.key_to_str(key))
  #print("**** "+cipher_utils.decrypt(cipher_text, key))
  new_key=change_key_aux(key, cipher_text, plain_alphabet)
  while re.search("[^A-Z]", cipher_utils.decrypt(cipher_text, new_key)):
    #print("OLD: "+cipher_utils.key_to_str(new_key))
    #print(cipher_utils.decrypt(cipher_text, new_key))
    new_key=change_key_aux(key, cipher_text, plain_alphabet)
    #print("NEW: "+cipher_utils.key_to_str(new_key))
    #print(cipher_utils.decrypt(cipher_text, new_key))
  return new_key
  
def fast_lex_eval(text, lexicon):
  score=0
  for w in lexicon:
    if w in text:
      score+=math.pow(len(w),1)
  return score/len(text)
  
def compute_score(quad_score, text):
    if re.search("[^A-Z]", text): # dump keys with only partial replacements
      return -999999

    lexicon_score=fast_lex_eval(text,my_lexicon)
    weight=0.17 # higher weight: more relevance of quadgrams 20:0.0196/-87.36784; 50:0.0286/-83
    # favor solutions resulting in longer text
    return -14+quad_score/(weight+math.pow(lexicon_score,1)) # 0.3:0.0196/-87.36784; 0.5:0.0286/-83 *math.pow(len(text),0.4)
    
def no_lex_compute_score(quad_score, text):
  weight=50 # higher weight, more relevance of quad_score
  # favor solutions resulting in longer text
  return quad_score/(weight+math.pow(len(text),0.05))
  
def score_from_cache(quad_score, text):
  if text in my_cache:
    final_score=my_cache[text]
    del my_cache[text]
    my_cache[text]=final_score #refresh value
    #print("CACHED "+str(len(my_cache)))
  else:
    if len(my_cache)>5000:
      del my_cache[list(my_cache.keys())[0]]
    final_score=compute_score(quad_score, text)
    my_cache[text]=final_score
  return final_score
  
  
def score(quad_score, plain_text):
  return score_from_cache(quad_score, plain_text)


