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

# Example usage:

word_list = word_list = ["the", "seal", "pear", "these", "all","light", "rainbow", "rain", "bow"]
for input_string in ["theseal","theXXseal","XXtheXXseal", "theXXsealX", "theseall",\
   "XtheseallX","theseallight","thesealight", "lightheseal", "lightXXseal", "rainbow"]:
#for input_string in ["lightheseal"]:
  print(" ")
  print("input_string:", input_string)
  total_gaps, result = word_break_with_gaps(input_string, word_list)

  print("Total Gaps:", total_gaps)
  print("Words:", result)

