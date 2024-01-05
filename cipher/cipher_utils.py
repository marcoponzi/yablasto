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
    
def evaluate_by_lexicon(best_plain, lexicon, longest_word, lexicon_avg_len, is_print=False):
	#lexicon, longest_word, lexicon_avg_len=load_lexicon(ARG_LANG,4,30000)
	##print(lexicon[:10])
	gaps,split_words=word_break_with_gaps(best_plain,lexicon)
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
	perc_covered=(len(best_plain)-gaps)/len(best_plain)
	perc_max_len=len(longest_found)/len(longest_word)
	perc_avg_len=float(avg_len)/float(lexicon_avg_len)
	#final_perc=perc_covered*ttr*(perc_max_len+perc_avg_len)/2.0
	#final_perc=ttr*perc_avg_len*(perc_covered+perc_max_len)/2
	final_perc=perc_avg_len*perc_covered*perc_max_len
	if is_print:
	  print(str(gaps)+" "+str(split_words))
	  print(longest_found+" "+longest_word)
	  print("average_len lexicon:"+str(lexicon_avg_len)+" deciphered:"+str(avg_len)) 
	  print("covered%: "+str(perc_covered))
	  print("max_word_len%: "+str(perc_max_len))
	  print("avg_word_len%: "+str(perc_avg_len))
	  print("ttr: "+str(ttr))
	  print("FINAL%: "+str(final_perc))
	return final_perc
