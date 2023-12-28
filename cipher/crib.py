import random
import cipher.cipher_utils as cipher_utils
import sys
import math
import re
#import cipher.verbosebigr as verbosebigr

oldcrib=['ARIES', 'TAURUS', 'GEMINI', 'CANCER', 'LEO', 'VIRGO', 'LIBRA', 'SCORPIUS', 'SAGITTARIUS', 'CAPRICORNUS', 'AQUARIUS', 'PISCES']

#global crib_module, CRIB
#global CRIB

# db.py
import sys

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it 
this.crib_module = None
this.CRIB = None

def set_module(m, crib_text, lang):
  #global  crib_module
  print(m)
  this.crib_module=m
  this.CRIB=cipher_utils.load_crib(crib_text+'.'+lang)
  print("CRIB "+str(this.CRIB))

######
''' create Initial key '''
def init_key(cipher_text, plain_alphabet):
    return this.crib_module.init_key(cipher_text, plain_alphabet)
    #global  crib_module
    #print(crib_module)    
    # met = getattr(crib_module, 'init_key')
    # return met(cipher_text, plain_alphabet)
    

######
''' swap 2 letters '''
def change_key(key, cipher_text, plain_alphabet):
  return crib_module.change_key(key, cipher_text, plain_alphabet)
  
def score(quad_score, plain_text):
  orig_score=crib_module.score(quad_score, plain_text)
  trigrams=0
  found_words=0
  found_parts=0
  for w in this.CRIB:
    if w in plain_text:
        found_words+=1
    found=False
    for i in range(0,len(w)-2):
      # print(w+" "+w[i:i+3])
      if w[i:i+2] in plain_text:
        trigrams+=1
        if not found:
          found=True
          found_parts+=1
          
  return 1*trigrams + found_parts+ 3*found_words + orig_score

