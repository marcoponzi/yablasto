import re


    
# longer keys first
def sort_dict(indict):
  new_d = {}
  klist=list(indict.keys())
  klist=sorted(klist) #alphabetical
  klist=sorted(klist, key=len, reverse=True) #longer first

  for k in klist:
    new_d[k] = indict[k]

  return new_d
  
def position_in_list(in_list, item):
  index=-1
  try:
    index = in_list.index(item)
  except ValueError as error:
    return index
  return index
  
def key_to_str(mydict):
  res=''
  for k in mydict.keys():
    res+=str(k)+":"+str(mydict[k])+" "
  return res
  
def load_crib(fname):
    words=list()
    with open("texts/examples/"+fname, "r") as infile:
        for line in infile:
            w = line.split("\n")[0]
            words.append( w.upper() )
    return sorted(sorted(words), key=len, reverse=True)
    
def word_break_with_gaps(s, word_list):
    word_set = set(word_list)
    n = len(s)
    dp = [None] * (n + 1)
    dp[0] = (0, [])  # (total_gaps, words)

    for str_end in range(1, n + 1):
        closest_index=0
        for str_start in range(str_end):
            if dp[str_start] is not None:
              closest_index=str_start
              #print(dp)
              #print("str_start:"+str(str_start)+" str_end:"+str(str_end)+" closest:"+str(dp[str_start])+" "+s[str_start:str_end])
            if s[str_start:str_end] in word_set:
                total_gaps, words = dp[closest_index]
                new_gaps = total_gaps + (str_start -closest_index)  # Count gaps if not at the beginning
                # longer words are found first, "rainbow" is preferred to "rain" "bow"
                if dp[str_end] is None or (dp[str_end][0]>new_gaps): 
                  dp[str_end] = (new_gaps, words + [s[str_start:str_end]])
                  #print(" WORD str_end:"+str(str_end)+" "+str(dp[str_end]))
            else:                
                total_gaps, words = dp[closest_index]
                new_gaps=total_gaps+str_end-closest_index
                if dp[str_end] is None or (dp[str_end][0]>new_gaps): 
                  gap_str='<'+s[closest_index:str_end]+'>'
                  dp[str_end] = (new_gaps, words+[ gap_str ])

    return dp[n]
    
def load_lexicon(lang, min_word_len=3, max_words=5000): #4 5000
    words=list()
    longest_word=''
    tot_chars=0
    lexicon_freq=dict()
    max_count=-1
    with open("languages/"+lang+".lexicon", "r") as infile:
        for line in infile: #remove counts, if present
            #word=re.sub(" .*","",line.split("\n")[0]).upper()
            word,num_str=line.split(' ')
            count=float(num_str)
            if max_count==-1:
              max_count=count
            count=count/max_count
            lexicon_freq[word]=count
            if len(word)>=min_word_len and len(words)<max_words:
              words.append(word)
              tot_chars+=len(word)
              if len(word)>len(longest_word):
                longest_word=word
    return words, longest_word, float(tot_chars)/float(len(words)), lexicon_freq
    

# key is a map: key:cipher-symbol, val:plain-text symbol
#  sorted by decreasing key length
def decrypt(cipher_text, key):
    plain=cipher_text
    for cipher_bit in key.keys():
      plain=re.sub(cipher_bit, key[cipher_bit],plain)
    plain = re.sub('_', '',plain) # remove nulls
    return plain
    
def evaluate_by_lexicon(plain_text, lexicon, longest_word, lexicon_avg_len, is_print=False):
	#lexicon, longest_word, lexicon_avg_len=load_lexicon(ARG_LANG,4,30000)
	##print(lexicon[:10])
	gaps,split_words=word_break_with_gaps(plain_text,lexicon)
	longest_found=''
	tot_chars=0
	found_words=list()
	for w in split_words:
	  if w[0]!='<' :
	    tot_chars+=len(w)
	    found_words.append(w)
	    if len(w)>len(longest_found):
	      longest_found=w
	avg_len=0
	ttr=0
	if len(found_words)!=0: 
	  avg_len=float(tot_chars)/float(len(found_words)) 
	  ttr=len(set(found_words))/len(found_words)
	perc_covered=(len(plain_text)-gaps)/len(plain_text)
	perc_max_len=len(longest_found)/len(longest_word)
	perc_avg_len=float(avg_len)/float(lexicon_avg_len)
	#final_perc=perc_avg_len*perc_covered*perc_max_len
	final_perc=pow(perc_covered,2)*perc_avg_len*perc_max_len
	if is_print:
	  print(str(gaps)+" "+str(split_words))
	  print("len: "+str(len(plain_text))+" longest:"+longest_found+" "+longest_word)
	  print("average_len lexicon:"+str(lexicon_avg_len)+" deciphered:"+str(avg_len)) 
	  print("covered%: "+str(perc_covered)+"  ttr: "+str(ttr))
	  print("max_word_len%: "+str(perc_max_len)+"  avg_word_len%: "+str(perc_avg_len))
	  print("FINAL%: "+str(final_perc))
	return final_perc
