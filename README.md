# 

based on blasto by Merricx https://github.com/Merricx/blasto

based on blasto_mini by user RobGea on this forum: https://www.voynich.ninja/thread-3637-post-52342.html#pid52342


lower case plain text converted to upper case cipher
cat slowbrowncat.eng | source encode_simple_sub.sh 

quadgrams/lat.uv.quadgrams: U replaced with V; rare characters K and W removed

quadgrams/lat.uv.e.quadgrams: OE and AE replaced with E (before removing spaces)


COMPUTE SCORE OF PLAIN TEXT ACCORDING TO CIPHER METHOD (syl):

time python3.6 yablasto.py lat texts/examples/desine.lat syl score 

SIMPLE SUBSTITUTION:

time python3.6 yablasto.py lat texts/examples/desine.lat.simple simplesub 50  > tmp/out.simplesub

SOME BIGRAMS USED AS VERBOSE CIPHER SYMBOLS:

time python3.6 yablasto.py lat texts/examples/desine.lat.verbose verbosebigr 400 > tmp/out.verbosebigr

UP TO 1/3 OF CIPHER CHARACTERS ARE NULLS:

time python3.6 yablasto.py eng texts/examples/letthewaters.eng.nulls nulls  400  > tmp/out.nulls

HOMOPHONIC CIPHER WHERE EACH PLAIN TEXT CHARACTER IS ENCODED AS A SYLLABLE/SHORT WORD (ONE TO MANY):

time python3.6 yablasto.py eng texts/examples/thesearethegenerations_long.eng.syl syl 400 > tmp/out.syl
