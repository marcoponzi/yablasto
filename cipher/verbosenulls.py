import random
import cipher.cipher_utils as cipher_utils
import cipher.verbosebigr as verbosebigr
import sys
import math
import string
import copy

my_lexicon=''
my_longest_word=''
my_lexicon_avg_len=''
my_cache=''

# return a character or bigram
def rand_cipher_bit(key,cipher_text, plain_alphabet):
  bigr_probability=.68 #.70 aaa
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
    for char in characters:
      cipher_bit=verbosebigr.rand_cipher_bit(key,cipher_text, plain_alphabet,.2)
      key[cipher_bit]=char
    
    return cipher_utils.sort_dict(key)

######
''' swap 2 letters '''
def change_key(key, cipher_text, plain_alphabet): 
  klist=list(key.keys())
  rand=random.random()
  if rand>.95: # add or remove key .90 ddd
        diff=list(set(plain_alphabet)-set(key.values()))
        nulls_bigr=list(key.values()).count('_')
        max_nulls_bigr=len(plain_alphabet)/3
        for k in list(key.keys()):
          if len(k)>1:
            nulls_bigr+=1
        if nulls_bigr<max_nulls_bigr and random.random()>.40:  #bbb .60
          diff=diff+['_'] # possibly add a null
        ###print(str(len(diff))+" > "+str(len(plain_alphabet)/2))
        if nulls_bigr<max_nulls_bigr and len(diff)>0 and (len(diff)>len(plain_alphabet)/2 or random.random()>.75): # .65 eee
          key[rand_cipher_bit(key,cipher_text, plain_alphabet)]=random.choice(diff)
        else:
          remove=random.choice(list(key.keys()))
          if len(remove)==1: #favour bigrams
            remove=random.choice(list(key.keys()))
          del key[remove]
  elif rand>.20: #.10 ccc
        # swap values for two keys
        i = random.choice(klist)
        j = random.choice(klist)
        count=0
        while key[i]==key[j] and count<999:
          j = random.choice(klist)
          count+=1
        temp = key[i]
        key[i] = key[j]
        key[j] = temp
  else: # change key for one value
    k = random.choice(klist)
    if len(k)==1: #favour bigrams
      k = random.choice(klist)
    temp=key[k]
    newkey=rand_cipher_bit(key,cipher_text, plain_alphabet)  
    while newkey==k:
      newkey=rand_cipher_bit(key,cipher_text, plain_alphabet)  
    del key[k]
    key[newkey]=temp
     
  return cipher_utils.sort_dict(key)
  
def compute_score(quad_score, text):
    lexicon_score=cipher_utils.evaluate_by_lexicon(text, my_lexicon, my_longest_word, my_lexicon_avg_len)
    weight=2.0 # higher weight: more relevance of quadgrams 20:0.0196/-87.36784; 50:0.0286/-83
    # favor solutions resulting in longer text
    return quad_score/(weight+math.pow(lexicon_score,1)) # 0.3:0.0196/-87.36784; 0.5:0.0286/-83 *math.pow(len(text),0.4)
  
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


