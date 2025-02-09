#!/usr/bin/env python -*-coding: utf-8-*-
# based on blasto by Merricx https://github.com/Merricx/blasto
# based on blasto_mini by user RobGea on this forum: https://www.voynich.ninja/thread-3637-post-52342.html#pid52342

import random, time, math, re, sys, copy
from math import log10
from collections import Counter
import itertools
import string
import datetime

#from split_into_words import word_break_with_gaps

import cipher.simplesub as simplesub
import cipher.simplesubanagr as simplesubanagr
import cipher.verbosebigr as verbosebigr
import cipher.nulls as nulls
import cipher.verbosenulls as verbosenulls
import cipher.cipher_utils as cipher_utils
import cipher.crib as crib
import cipher.syl as syl
#import cipher.cipher_utils as cipher_utils

import importlib

sys.path.insert(2, 'cipher')


# delay time in seconds
sleep = 0

def frmt(myfloat,dec=5):
  # return "{:.5f}".format(myfloat)
  formstr="{:."+str(dec)+"f}"
  return formstr.format(myfloat)

def log(msg):
    time = datetime.datetime.now()
    display_time = time.strftime("%H:%M:%S")
    print("LOG:"+display_time+" "+str(msg))


def load_quadgrams(lang):
    store = []
    with open("languages/"+lang+".quadgrams", "r") as infile:
        for line in infile:
            qgramz = line.split("\n")[0]
            store.append( qgramz )
    return store


def parse_qgram(lang, is_anagr):
    # create dict of ngram strings : ints
    ngrams = {}
    plain_alphabet=set()
    qtot = 0
    txt = load_quadgrams(lang)
    for line in txt:
        tmp = line.split(' ')
        qgm_count = int(tmp[1])
        ngrams[tmp[0]] = qgm_count
        plain_alphabet.update(set(list(tmp[0])))
        qtot += qgm_count

    ################
    # 456976 combos
    # generate all 4-gram combos from A-Z
    # if combo not in ngram dict then add it
    chars = string.ascii_uppercase
    if is_anagr:
      chars=chars+','
    print("Chars: "+str(chars))
    orderings = list(itertools.product(chars, repeat=4))
    #print(orderings[:100])
    cntr = 0
    for i in orderings:
        it = ''.join(i)
        if it in ngrams:
            pass
        else:
            ngrams[it] = .1
            # how many ngrams have we added
            cntr += .1

    ################
    # convert quadgrams dict
    # into list of tuples for easy lambda sort
    ngrams2 = []
    for k, v in ngrams.items():
        tup = (k, v)
        ngrams2.append(tup)
    ngrams2.sort(key = lambda i:i[0])

    ################
    # calculate and keep log probabilities in new list
    qgram = []
    for i in ngrams2:
        v = i[1]
        qlf = v / ( qtot + cntr)
        log = log10(float( qlf ) )
        qgram.append(log)
    if is_anagr:
      assert len(qgram) == 531441, 'qgram anagram list size error'
    else:
      assert len(qgram) == 456976, 'qgram list size error'

    if ',' in plain_alphabet:
      plain_alphabet.remove(',')
    return qgram, list(plain_alphabet)



def clean_input(ciphertext):
    text = re.sub("[ \n]","",ciphertext)
    return text

def decrypt2(cipher_text,parent_key, is_anagr):
  plain_text=cipher_utils.decrypt(cipher_text,parent_key)
  if is_anagr:
    plain_text=simplesubanagr.do_anagrams(plain_text)
  return plain_text

def hill_climbing(cipher_text, plateau, sleep, parent_key,perc_progress, module):
    child_key = ""
    best_score, ignore = score_text(decrypt2(cipher_text,parent_key, is_anagr ), module)
    ## best_score = -99999 #-72.6613499895892
    best_key=parent_key # -85.74
    parent_score=best_score

    GO = True
    count=0
    consec_fails = 0
    while GO:
        child_key = module.change_key(copy.deepcopy(parent_key),cipher_text, plain_alphabet)
        child_score, ignore = score_text(decrypt2(cipher_text,child_key, is_anagr ), module)
        if child_score > best_score or (child_score==best_score and len(child_key)<len(best_key)):
          ### log("child better: "+str(child_score)+" best: "+str(best_score))
          consec_fails = 0
          best_score = child_score
          best_key=child_key
          parent_score=child_score
          parent_key = child_key
        else:
          consec_fails  += 1

          # accept child_key if the new score is better or only marginally worse
          curr_temperature=(0.25+(1-perc_progress)*ARG_TEMPERATURE/20.0-pow(perc_progress,ARG_TEMPERATURE)/4)
          if best_score!=0 and (child_score < best_score) and \
             abs((best_score-child_score)/best_score)<curr_temperature:
            ## abs((best_score-child_score)/best_score)<(0.21-(perc_progress*perc_progress)/4):
            ## log("child worse: "+str(child_score)+" best: "+str(best_score))
            parent_score=child_score
            parent_key = child_key

        time.sleep( sleep )

        if consec_fails >= plateau: 
            log("Reached local minima.Restarting...:"+str(count)+" Temperature:"+str(curr_temperature))
            GO = False
        if count >= plateau*5: # TODO check if this breaks verbosebigr or other ciphers
            log("Max iterations.Restarting...:"+str(count)+" Temperature:"+str(curr_temperature))
            GO = False        
        count+=1

    log("curr_parent: "+str(parent_score)+" "+cipher_utils.key_to_str(parent_key))
    result=dict()
    result['key'] = best_key
    result['plain'] = decrypt2(cipher_text, best_key, is_anagr)
    result['score'] = best_score
    return result

def get_quad_val(alpha,text,i,temp,l,l2,l3):
        temp[0] = alpha.find(text[i])
        temp[1] = alpha.find(text[i+1])
        temp[2] = alpha.find(text[i+2])
        temp[3] = alpha.find(text[i+3])
        pos=(l3)*temp[0] + (l2)*temp[1] + l*temp[2] + temp[3]
        val=qgram[pos]
        return val,pos


#####################
def score_text(text, module):
    # [M] handling unreplaced characters as Z TODO
    # comma , as word separator for anagrams
    text=re.sub('[^A-Z, ]','@',text)
    if is_anagr:
      text=simplesubanagr.do_anagrams(text.upper().replace(' ',','))
      alpha = ",ABCDEFGHIJKLMNOPQRSTUVWXYZ" # comma ',' word separator
    else:
      alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
     
    temp = [0,0,0,0]
    score = 0
    l=len(alpha)
    l3 = l**3
    l2 = l**2
    best_val=-99999999
    best_quad='____'
    for i in range(0,len(text)-3):
      val=-5*len(text)
      if '@' in text[i:i+4]:
        score-=len(text)*5 # unrecognized characters
      else:
        val,pos=get_quad_val(alpha,text,i,temp,l,l2,l3)
        score += val**3
      ## print("score plus "+text[i:i+4]+" "+str(score))
    quad_score=score/float(max(0.001,len(text)-3)) # max: avoid division by zero
    ##print("SCORE "+str(score)+" "+best_quad+" "+str(best_val))
    return module.score(quad_score,text),quad_score
    

def evaluate_by_lexicon2(plain_text,lexicon, longest_word, lexicon_avg_len, is_anagr):
  print(plain_text)
  if is_anagr:
    plain_text=simplesubanagr.do_anagrams(plain_text.upper().replace(' ',','))
    print("ANAGR:: "+plain_text)
  return cipher_utils.evaluate_by_lexicon(plain_text, lexicon, longest_word, lexicon_avg_len, True)


#############################################
#Initial variables
result = {'key':'','plain':'','score':''}
best_score = -99999
best_plain = ""
best_res=dict()
best_res['score']=best_score
best_res['plain']='_'
best_res['key']=dict()

ARG_LANG=sys.argv[1]
ARG_CTEXT_FILE=sys.argv[2]
ARG_MODULE=sys.argv[3]
ARG_RESTARTS=sys.argv[4]
CRIB_MODULE=''
ctext=''
with open(ARG_CTEXT_FILE, "r") as infile:
  for line in infile:
    ctext+=line

is_anagr=(ARG_MODULE=='simplesubanagr')
if is_anagr:
  qgram,plain_alphabet = parse_qgram(ARG_LANG,True)
else:
  qgram,plain_alphabet = parse_qgram(ARG_LANG,False)

log(' ')

plains=set(result['plain'])

##################   META  #######
''' https://en.wikipedia.org/wiki/Hill_climbing#Variants
 Random-restart hill climbing '''
meta = []

lexicon, longest_word, lexicon_avg_len, lexicon_freq=cipher_utils.load_lexicon(ARG_LANG)
if ARG_MODULE.startswith('crib_'):
  module=crib
  ignore,crib_text,module_name=ARG_MODULE.split('_')
  log(crib_text)
  crib_module=importlib.import_module("cipher."+module_name)
  log('CRIB_MODULE '+str(crib_module))
  crib.set_module(crib_module, crib_text, ARG_LANG)
  ##lexicon=crib.CRIB+lexicon #add crib words to lexicon
  if module_name=='verbosenulls': # TODO factory method to create modules?
    crib_module.set_lexicon(lexicon, longest_word, lexicon_avg_len)
elif ARG_MODULE=='simplesub':
  module=simplesub
elif ARG_MODULE=='simplesubanagr':
  module=simplesubanagr
  module.set_lexicon_freq(lexicon_freq, longest_word, lexicon_avg_len)
elif ARG_MODULE=='verbosebigr':
  module=verbosebigr
elif ARG_MODULE in ['verbosenulls','simplesubanagr']:
  module=verbosenulls
  module.set_lexicon(lexicon, longest_word, lexicon_avg_len)
elif ARG_MODULE=='nulls':
  module=nulls
elif ARG_MODULE=='syl':
  module=syl
else:
  log("Unknown module "+ARG_MODULE)

if is_anagr:
  cipher_text=re.sub('[\n ]*$','',ctext)
  cipher_text = cipher_text.replace(' ',',') # comma , as word separator
else:
  cipher_text = clean_input(ctext)
log('cipher text:'+cipher_text)
log(' ')

if ARG_RESTARTS=='score':
  evaluate_by_lexicon2(cipher_text.upper(), lexicon, longest_word, lexicon_avg_len, is_anagr)
  tot_score, quad_score=score_text(cipher_text.upper(),module)
  print("QUAD_SCORE: "+frmt(quad_score)+" TOT_SCORE: "+frmt(tot_score))
  sys.exit()
  # Number of hill climber restarts
else:
  ARG_TEMPERATURE=float(sys.argv[5]) #in range {0..5}, typically 3
  
restarts = int(ARG_RESTARTS) # 300

# hill climber #
# stop after plateu consecutive iters w/o score increase
plateau = 600+restarts*5 #100+restarts*10

for restart in range(restarts ):
     perc_progress=float(restart+0.01)/restarts

     if perc_progress<=.15: # .1 initial random keys
        parent_key = module.init_key(cipher_text, plain_alphabet)
        log("")
        initial_out=decrypt2(cipher_text,parent_key, is_anagr )
        best_score, ignore = score_text(initial_out, module)
        log("initial score:"+str(best_score))
        evaluate_by_lexicon2(initial_out, lexicon, longest_word, lexicon_avg_len, is_anagr)
        log("RAND KEY "+cipher_utils.key_to_str(parent_key))
     else: # refining current best key
        parent_key=copy.deepcopy(best_res['key'])
        log("")
        log("BEST KEY "+cipher_utils.key_to_str(parent_key))
     result = hill_climbing(cipher_text, plateau, sleep, parent_key,perc_progress,module)
     if result['key']!=best_res['key'] and result['score']>=best_res['score']: #if equal score, new key is shorter
       log(" *** old "+frmt(best_res['score'])+" "+str(best_res['plain']))
       log(" *** new "+frmt(result['score'])+" "+str(result['plain']))
       log(" old key "+cipher_utils.key_to_str(best_res['key']))
       log(" new key "+cipher_utils.key_to_str(result['key']))
       best_res=result

     tup = (result['score'],restart,result['plain'], cipher_utils.key_to_str(result['key']) )
     if (not(result['plain'] in plains)):
       plains.add(result['plain'])
       meta.append(tup)
     log(str(restart)+"/"+str(restarts)+" "+str(tup))
     sys.stdout.flush()

log(' ')
meta.sort()
for i in meta:
    log(i)
log(' ')

best_plain=best_res['plain']
log("best_plain: "+str(best_plain))

evaluate_by_lexicon2(best_plain.upper(), lexicon, longest_word, lexicon_avg_len, is_anagr)
tot_score, quad_score=score_text(best_plain,module)
print("QUAD_SCORE: "+frmt(quad_score)+" TOT_SCORE: "+frmt(tot_score))










