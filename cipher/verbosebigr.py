import random
import cipher.cipher_utils as cipher_utils
import sys
import math
import string

bigr_prob=.40 #.6 aaa

# return a character or bigram
def rand_cipher_bit(key,cipher_text, plain_alphabet, bigr_probability):
      text_list=list(cipher_text)
      cipher_bit=''
      rand=random.random()

      if rand >bigr_probability: # character .6 52.1
        cipher_bit=random.choice(text_list)
        count=0
        while cipher_bit in key.keys() and count<10:
          cipher_bit=random.choice(text_list) # pick based on frequency
          count+=1
        if cipher_bit in key.keys(): # pick a character that is not a key yet
          diff=set(text_list).difference(set(key.keys()))
          if len(diff)>0:
            cipher_bit=random.choice(list(diff))
          else:
            cipher_bit=''
      if cipher_bit=='': # bigram
        pos=random.randint(0,len(cipher_text)-1)
        cipher_bit=cipher_text[pos:pos+2]
        count=0
        while cipher_bit in key.keys() and count<999999:
          pos=random.randint(0,len(cipher_text)-1)
          cipher_bit=cipher_text[pos:pos+2]
          count+=1
      if cipher_bit in key.keys():
        print("ERROR for verbose sequence: '"+cipher_bit+"'")
        sys.exit()
      return cipher_bit

######
''' create Initial key '''
def init_key(cipher_text, plain_alphabet):
    global bigr_prob
    key=dict()
    for char in plain_alphabet:
      cipher_bit=rand_cipher_bit(key,cipher_text, plain_alphabet, bigr_prob)
      key[cipher_bit]=char
    
    return cipher_utils.sort_dict(key)

######
''' swap 2 letters '''
def change_key(key, cipher_text, plain_alphabet):
  global bigr_prob
  klist=list(key.keys())
  rand=random.random()
  if rand>.60: # 80 bbb
        diff=list(set(plain_alphabet)-set(key.values()))
        #if len(diff)>0 and random.random()>pow(float(len(key))/float(len(plain_alphabet)),2): # 2: 52.1
        if len(diff)>0 and random.random()>.2: #.01:-49.8
          key[rand_cipher_bit(key,cipher_text, plain_alphabet, bigr_prob)]=random.choice(diff)
        else:
          del key[random.choice(list(key.keys()))]
  elif rand>.30: # 30 CCC
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
    newkey=rand_cipher_bit(key,cipher_text, plain_alphabet, bigr_prob)
    while newkey==k:
      newkey=rand_cipher_bit(key,cipher_text, plain_alphabet, bigr_prob) 
    del key[k]
    key[newkey]=temp

  return cipher_utils.sort_dict(key)
  
def score(quad_score, plain_text):
  # favor solutions resulting in longer text
  return quad_score/(math.pow(len(plain_text),0.1))

