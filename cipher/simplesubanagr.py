import random
import cipher.cipher_utils as cipher_utils
import cipher.simplesub as simplesub
import re
import math

my_lexicon=''
my_longest_word=''
my_lexicon_avg_len=''

def set_lexicon(lexicon_freq, longest_word, lexicon_avg_len):
  print("simplesubanagr set_lexicon_freq")
  global my_longest_word
  global my_lexicon_freq
  global my_lexicon_avg_len
  my_lexicon_freq=lexicon_freq
  my_longest_word=longest_word
  my_lexicon_avg_len=lexicon_avg_len

# , as word separator

######
def init_key(cipher_text, plain_alphabet):
    no_sep=re.sub(',','',cipher_text)
    return simplesub.init_key(no_sep,plain_alphabet)
    #key=dict()
    #cipher_alphabet=sorted(list(set(list(no_sep))))
    #for cipher_char in cipher_alphabet:
    #  key[cipher_char]=cipher_char.upper()
    #return key

######
# change a single plain character
def change_key(key, cipher_text, plain_alphabet):
    return simplesub.change_key(key, cipher_text, plain_alphabet)
    
## def score(quad_score, plain_text):
##  return quad_score
  
def score(quad_score, plain_text):
  words=plain_text.split(',') 
  score=quad_score
  l_lex=len(my_lexicon)
  lex_words=my_lexicon_freq.keys()
  quad_weight=1 # higher values favor quads over lexicon
  for w in words:
    if w in lex_words:
      freq=my_lexicon_freq[w]
      lex_score=0.2*len(w)*(quad_weight+math.pow(freq,0.5))
      score+=lex_score
      ##print("FOUND W: "+w+" freq: "+str(freq)+" lex_score: "+str(lex_score))
  return score

# comma , as word separators
def do_anagrams(text):
  text=re.sub('[^A-Z,]','@',text)
  res=''
  for w in text.split(','):
    res+=''.join(sorted(list(w)))+","
  res=re.sub(',,*$','',res)
  return res
  

