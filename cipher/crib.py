import random
import cipher.cipher_utils as cipher_utils
from cipher.cipher_utils import my_log
import sys
import math
import re
import Levenshtein
import copy
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

  
def load_crib(fname):
    words=list()
    with open("texts/cribs/"+fname, "r") as infile:
        for line in infile:
            w = line.split("\n")[0]
            words.append( w.upper() )
    return sorted(sorted(words), key=len, reverse=True)

def set_module(m, crib_text, lang):
  #global  crib_module
  print(m)
  this.crib_module=m
  this.CRIB=list()
  for line in load_crib(crib_text+'.'+lang):
    line=line.replace(',',' ')
    for w in line.split(' '):
      if len(w)>0 and not w in this.CRIB:
        this.CRIB.append(w)
  this.CRIB=list(reversed(sorted(this.CRIB, key=len)))
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
  
def count_exact_words(plain_text):
  found_words=list()
  is_comma=False
  separator=''
  crib_copy=copy.deepcopy(this.CRIB)
  if ',' in plain_text:
    is_comma=True
    plain_text=','+plain_text+','
    separator=','
  for w in this.CRIB: # find and remove whole words
    ##print([separator+w+separator , plain_text])
    if separator+w+separator in plain_text:
        ##print("foundWord: "+w)
        found_words.append(w)
        crib_copy.remove(w) # remove from crib when found
        ## ngrams+=len(w)
        plain_text=plain_text.replace(w,'')
  return found_words,plain_text,crib_copy
  
def find_ngrams(plain_text,N):
  ngrams=list()
  for w in this.CRIB:    
    to_remove=list()  
    start,end=-9999,-9999
    for i in range(0,len(w)-N+1):
      ##my_log(w[i:i+N])
      if w[i:i+N] in plain_text:
        start,end,to_remove=ngram_found(w[i:i+N],plain_text,N,start,end,to_remove)
        ngrams.append(w[i:i+N])
        ##my_log(w[i:i+N]+" "+str(ngrams))
    if start>=0:
      ##my_log("adding: "+str([start,end]))
      to_remove.append([start,end])
    to_remove.reverse()
    for start,end in to_remove:
      ##my_log("to_remove: "+str(to_remove)+" "+plain_text)
      plain_text=plain_text[0:start]+plain_text[end:len(plain_text)]
      ## print("removed: "+plain_text)
  return ngrams
  
def get_words_for_crib(plain_text,crib_word):
  res=list()
  if ',' in plain_text:
    for w in plain_text.split(','):
      if len(w)>0:
        res.append(w)
  else:
    for i in range(0,1+len(plain_text)-len(crib_word)):
      res.append(plain_text[i:i+len(crib_word)])
  # my_log(str(res)+" "+crib_word+" "+plain_text)
  res = sorted(list(set(res)))
  ##my_log("get_words_for_crib: "+str(res))
  return res
  
def find_partial_words(plain_text,cur_crib):
  res=dict()
  text_copy=copy.deepcopy(plain_text)
  cur_crib=copy.deepcopy(cur_crib)
  cur_crib.sort()
  cur_crib=sorted(cur_crib, key=len, reverse=True) #decreasing len
  for cr_w in cur_crib:
    candidates=get_words_for_crib(text_copy,cr_w)
    candidates.sort()
    candidates = sorted(candidates, key=len, reverse=True) #decreasing len
    ## my_log("CANDIDATES: "+str(candidates))
    for cand in candidates:
      min_len=min(len(cr_w),len(cand))
      if (cr_w in cur_crib) and abs(len(cand)-len(cr_w))<min_len/2 and min_len>3:
        max_len=max(len(cr_w),len(cand))
        ratio=1.0-(Levenshtein.distance(cand,cr_w)/max_len)
        if  ratio>.6:
          my_log(["Partial: ",cand,cr_w,ratio])
          res[cand+'|crib:'+cr_w]=ratio*ratio*len(cr_w) # ratio squared
          text_copy=text_copy.replace(cand,'')
          cur_crib.remove(cr_w)
          
  return res
  
def score(quad_score, plain_text):
  plain_text=plain_text.replace(' ',',')
  my_log(plain_text)
  orig_len=len(plain_text)
  nw=len(plain_text.split(','))
  orig_score=crib_module.score(quad_score, plain_text)
  
  found_words,plain_text,cur_crib=count_exact_words(plain_text)
  partial_distances=find_partial_words(plain_text,cur_crib)
  part_nums=partial_distances.values()
  
  ##ngrams=find_ngrams(plain_text, 3) # 3=trigrams, 2=bigrams

  quad_weight=3 # 1 higher value, more weight to quad_score        
  #return 2*ngrams + found_parts+ 3*found_words + orig_score
  #my_log(partial_distances)
  my_log("orig_score: " +str(orig_score) + " partial_distances: "+str(partial_distances)+" words: "+str(found_words))
  return pow(nw*orig_len,0.7)*orig_score/\
     (quad_weight*orig_len+1*sum(part_nums) +3*pow(len(found_words)+len(''.join(found_words)),1.5))

