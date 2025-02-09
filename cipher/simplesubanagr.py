import random
import cipher.cipher_utils as cipher_utils
import cipher.simplesub as simplesub
import copy
import re

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
    
def score(quad_score, plain_text):
  return quad_score

# comma , as word separators
def do_anagrams(text):
  text=re.sub('[^A-Z,]','@',text)
  res=''
  for w in text.split(','):
    res+=''.join(sorted(list(w)))+","
  res=re.sub(',,*$','',res)
  return res
  

