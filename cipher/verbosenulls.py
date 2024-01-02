import random
import cipher.cipher_utils as cipher_utils
import sys
import math

# return a character or bigram
def rand_cipher_bit(key,cipher_text, plain_alphabet):
      text_list=list(cipher_text)
      cipher_bit=''
      rand=random.random()
      if rand>.9:
        cipher_bit=random.choice(plain_alphabet).lower()
        if cipher_bit in key.keys():
          cipher_bit=''
      elif cipher_bit=='' or rand >.5: # character
        cipher_bit=random.choice(text_list)
        count=0
        while cipher_bit in key.keys() and count<1000:
          cipher_bit=random.choice(text_list)
          count+=1
        if cipher_bit in key.keys():
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
    key=dict()
    nulls=[]
    for i in range(0,random.randint(0,int(len(plain_alphabet)/4))):
      nulls.append('_')
    for char in plain_alphabet+nulls:
      cipher_bit=rand_cipher_bit(key,cipher_text, plain_alphabet)
      key[cipher_bit]=char
    
    return cipher_utils.sort_dict(key)

######
''' swap 2 letters '''
def change_key(key, cipher_text, plain_alphabet):
  klist=list(key.keys())
  diff=set(plain_alphabet)-set(key.values())
  if random.random()>.05: # switch two cipher/plain couples
    switch = True
    while switch:
        i = random.choice(klist)
        j = random.choice(klist)
        temp = key[i]
        key[i] = key[j]
        key[j] = temp

        if key[i] != key[j]:
            switch=False
  elif len(diff)>0 and random.random()<.05: # replace with unused plain character
      #print("CHANGE")
      k=random.choice(klist)
      key[k]=random.choice(list(diff))
  elif list(key.values()).count('_')<len(key)/3 and random.random()<0.02: # add null
      k=rand_cipher_bit(key,cipher_text, plain_alphabet) 
      while (k in key.keys()) and key[k]=='_':
        k=rand_cipher_bit(key,cipher_text, plain_alphabet) 
      key[k]='_'
  else: # a new cipher_bit for a plain character
    k = random.choice(klist)
    temp=key[k]
    newkey=rand_cipher_bit(key,cipher_text, plain_alphabet)  
    while newkey==k:
      newkey=rand_cipher_bit(key,cipher_text, plain_alphabet)  
    del key[k]
    key[newkey]=temp

  return cipher_utils.sort_dict(key)
  
def score(quad_score, plain_text):
  weight=20 # higher weight, more relevance for quadgrams
  # favor solutions resulting in longer text and more varied alphabet (fewer nulls)
  return 100.0*quad_score/(weight+math.pow(len(plain_text),0.7)+math.pow(len(set(plain_text)),0.7))

