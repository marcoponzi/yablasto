from cipher.cipher_utils  import word_break_with_gaps

# Example usage:
if __name__ == "__main__":
	word_list = word_list = ["the", "seal", "pear", "these", "all","light", "rainbow", "rain", "bow"]
	for input_string in ["theseal","theXXseal","XXtheXXseal", "theXXsealX", "theseall",\
	   "XtheseallX","theseallight","thesealight", "lightheseal", "lightXXseal", "rainbow"]:
	#for input_string in ["lightheseal"]:
	  print(" ")
	  print("input_string:", input_string)
	  total_gaps, result = word_break_with_gaps(input_string, word_list)

	  print("Total Gaps:", total_gaps)
	  print("Words:", result)

