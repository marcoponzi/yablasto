#!/usr/bin/env python -*-coding: utf-8-*-
# based on blasto by Merricx https://github.com/Merricx/blasto
# based on blasto_mini by user RobGea on this forum: https://www.voynich.ninja/thread-3637-post-52342.html#pid52342

import random, time, math, re, sys, copy
from math import log10
from collections import Counter
import itertools
import string

import decipher.simplesub as simplesub
import decipher.verbosebigr as verbosebigr
import decipher.nulls as nulls
import decipher.syl as syl
import decipher.decipher_utils as decipher_utils

sys.path.insert(1, '/home/user/rec/voynich/python')
sys.path.insert(2, 'decipher')
from util import log, frmt


# delay time in seconds
sleep = 0

# feed the ROTate result into hill climber, little benefit
FEED = False


def loadfile(lang):
    store = []
    with open("quadgrams/"+lang+".quadgrams", "r") as infile:
        for line in infile:
            qgramz = line.split("\n")[0]
            store.append( qgramz )
    return store


def parse_qgram(lang):
    # create dict of ngram strings : ints
    ngrams = {}
    plain_alphabet=set()
    qtot = 0
    txt = loadfile(lang)
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
    orderings = list(itertools.product(chars, repeat=4))
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

    assert len(qgram) == 456976, 'qgram list size error'

    return qgram, list(plain_alphabet)



def clean_input(ciphertext):
    text = re.sub("[ \n]","",ciphertext)
    return text

# TODO Delete
def cached_score(cipher_text, key):
  return score_text(decipher_utils.decrypt(cipher_text,key))
  key_str=re.sub(" ","",key_to_str(key))
  if key_str in score_cache.keys():
    score = score_cache[key_str]
    ##print("CACHED")
  else:
    if len(score_cache)>100000:
      for k in list(score_cache.keys())[:10]:
        del score_cache[k]
    score=score_text(decipher_utils.decrypt(cipher_text,key))
    score_cache[key_str]=score
  return score

def hill_climbing(cipher_text, plateau, sleep, parent_key,perc_progress, module):
    child_key = ""
    best_score = score_text(decipher_utils.decrypt(cipher_text,parent_key ))
    ## best_score = -99999 #-72.6613499895892
    best_key=parent_key # -85.74
    parent_score=best_score

    GO = True
    count=0
    consec_fails = 0
    while GO:
        child_key = module.change_key(copy.deepcopy(parent_key),cipher_text, plain_alphabet)
        child_score = score_text(decipher_utils.decrypt(cipher_text,child_key ))
        if (child_score > best_score):
          ### log("child better: "+str(child_score)+" best: "+str(best_score))
          consec_fails = 0
          best_score = child_score
          best_key=child_key
          parent_score=child_score
          parent_key = child_key
        else:
          consec_fails  += 1

        # accept child_key if the new score is better or only marginally worse
        if (child_score < best_score) and (child_score/best_score)<(1.19-(perc_progress*perc_progress*perc_progress)/5):
            ## log("child worse: "+str(child_score)+" best: "+str(best_score))
            parent_score=child_score
            parent_key = child_key

        time.sleep( sleep )

        if consec_fails >= plateau: 
            log("Reached local minima.Restarting...:"+str(count))
            GO = False
        count+=1

    log("curr_parent: "+str(parent_score)+" "+key_to_str(parent_key))
    result=dict()
    result['key'] = best_key
    result['plain'] = decipher_utils.decrypt(cipher_text, best_key)
    result['score'] = best_score
    return result



#####################
def score_text(text):
    # [M] handling unreplaced characters as Z
    text=re.sub('[^A-Z]','Z',text)
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    temp = [0,0,0,0]
    score = 0
    #l = len(alpha)
    l=26
    l3 = l**3
    l2 = l**2

    for i in range(0,len(text)-3):
        temp[0] = alpha.find(text[i])
        temp[1] = alpha.find(text[i+1])
        temp[2] = alpha.find(text[i+2])
        temp[3] = alpha.find(text[i+3])
        val=qgram[(l3)*temp[0] + (l2)*temp[1] + l*temp[2] + temp[3]]
        score += val**3
    res=score/float(len(text)-3)
    ### log("SCORE "+str(text)+" "+str(res))
    #return res/float(math.sqrt(len(text)))
    #return res/(len(set(list(text)))*float(math.sqrt(len(text))))
    return 100.0*res/(math.pow(len(set(list(text))),0.7)*math.sqrt(len(text)))
    
def key_to_str(mydict):
  res=''
  for k in mydict.keys():
    res+=str(k)+":"+str(mydict[k])+" "
  return res

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
ARG_DECIPHER=sys.argv[3]
ARG_RESTARTS=sys.argv[4]
ctext=''
with open(ARG_CTEXT_FILE, "r") as infile:
  for line in infile:
    ctext+=line

qgram,plain_alphabet = parse_qgram(ARG_LANG)


cipher_text = clean_input(ctext)
log('cipher text:'+cipher_text)
log(' ')

# Number of hill climber restarts
restarts = int(ARG_RESTARTS) # 300

# hill climber #
# stop after plateu consecutive iters w/o score increase
plateau = 2000+math.sqrt(restarts)*20 


log(' ')

plains=set(result['plain'])

##################   META  #######
''' https://en.wikipedia.org/wiki/Hill_climbing#Variants
 Random-restart hill climbing '''
meta = []
if ARG_DECIPHER=='score':
  log(score_text(cipher_text.upper()))
  sys.exit()
elif ARG_DECIPHER=='simplesub':
  module=simplesub
elif ARG_DECIPHER=='verbosebigr':
  module=verbosebigr
elif ARG_DECIPHER=='nulls':
  module=nulls
elif ARG_DECIPHER=='syl':
  module=syl
else:
  log("Unknown module "+ARG_DECIPHER)

for restart in range(restarts ):
     perc_progress=float(restart+0.1)/restarts
     if perc_progress<.2: # or random.random()>(math.sqrt(perc_progress)*1.0): 
        parent_key = module.init_key(cipher_text, plain_alphabet)
        log("")
        log("RAND KEY "+key_to_str(parent_key))
     else:
        parent_key=copy.deepcopy(best_res['key'])
        log("")
        log("BEST KEY "+key_to_str(parent_key))
     result = hill_climbing(cipher_text, plateau, sleep, parent_key,perc_progress,module)
     if result['score']>best_res['score']:
       log(" *** old "+frmt(best_res['score'])+" "+str(best_res['plain']))
       log(" *** new "+frmt(result['score'])+" "+str(result['plain']))
       log(" old key "+key_to_str(best_res['key']))
       log(" new key "+key_to_str(result['key']))
       best_res=result

     tup = (result['score'],restart,result['plain'], key_to_str(result['key']) )
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











