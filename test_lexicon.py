import cipher.cipher_utils as cipher_utils
import time

def myeval(text, lexicon):
  score=0
  for w in lexicon:
    if w in text:
      score+=1
  return score/len(text)

lexicon, longest_word, lexicon_avg_len,lexicon_freq=cipher_utils.load_lexicon('eng')
texts=["inthebeginninggodcreatedtheheavenandtheearthandtheearthwaswithoutformandvoidanddarknesswasuponthefaceofthedeepandthespiritofgodmoveduponthefaceofthewaters",
"andgodsaidletthewatersundertheheavenbegatheredtogetheruntooneplaceandletthedrylandappearanditwasso",
"andherealicebegantogetrathersleepyand", "anotherlongpassageandthewhiterabbitwas"]
results=list()
start=time.time()*1000.0
for t in texts:
  results.append(cipher_utils.evaluate_by_lexicon(t.upper(), lexicon, longest_word, lexicon_avg_len, False))

print(str(time.time()*1000.0-start)+" "+str(results))

results=list()
start=time.time()*1000.0
for t in texts:
  results.append(myeval(t.upper(), lexicon))

print(str(time.time()*1000.0-start)+" "+str(results))
for w in ['AND', 'BUT', 'NEVER']:
  print(w+" "+str(lexicon_freq[w]))
