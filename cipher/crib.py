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
  
def ngram_found(ngram,plain_text,N,start,end,to_remove):
  index=plain_text.index(ngram)
  if start<0 or index>end: # not overlapping
    if start>=0:
      to_remove.append([start,end])
    start=index
    end=index+N
  elif index+N>end: #match is further right than previous match
    end=index+N
  ## print(ngram+" "+str(start)+" "+str(end))
  return start,end,to_remove
  
def score(quad_score, plain_text):
  orig_score=crib_module.score(quad_score, plain_text)
  ngrams=0
  N=2 # trigrams
  found_words=0
  found_parts=0
  for w in this.CRIB: # find and remove whole words
    if w in plain_text:
        ## print("foundWord: "+w)
        found_words+=1
        ngrams+=len(w)
        plain_text=plain_text.replace(w,'')

  for w in this.CRIB:    
    to_remove=list()  
    found=False
    start,end=-9999,-9999
    for i in range(0,len(w)-N+1):
      ## print(w[i:i+N])
      if w[i:i+N] in plain_text:
        start,end,to_remove=ngram_found(w[i:i+N],plain_text,N,start,end,to_remove)
        ngrams+=1
        ##print(w[i:i+N]+" "+str(ngrams))
        if not found:
          found=True
          found_parts+=1
    if start>=0:
      ##print("adding: "+str([start,end]))
      to_remove.append([start,end])
    to_remove.reverse()
    for start,end in to_remove:
      ## print("to_remove: "+str(to_remove)+" "+plain_text)
      plain_text=plain_text[0:start]+plain_text[end:len(plain_text)]
      ## print("removed: "+plain_text)
          
  #return 2*ngrams + found_parts+ 3*found_words + orig_score
  ##print("ngrams: "+str(ngrams)+" parts: "+str(found_parts)+" words: "+str(found_words))
  return orig_score/(1+ngrams + 0*found_parts+ 3*found_words)

