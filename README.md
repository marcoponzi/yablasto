# YET ANOTHER BLASTO

based on blasto by Merricx https://github.com/Merricx/blasto

based on blasto_mini by user RobGea on this forum: https://www.voynich.ninja/thread-3637-post-52342.html#pid52342

Source of English lexicon:

https://gist.github.com/h3xx/1976236


quadgrams/lat.uv.quadgrams: U replaced with V; rare characters K and W removed

quadgrams/lat.uv.e.quadgrams: OE and AE replaced with E (before removing spaces)


COMPUTE SCORE OF PLAIN TEXT ACCORDING TO CIPHER METHOD (syl):

python3.8 yablasto.py lat texts/examples/desine.lat syl score 

SIMPLE SUBSTITUTION:

python3.8 yablasto.py lat texts/examples/desine.lat.simplesub simplesub 50  2  > tmp/out.simplesub

SOME BIGRAMS USED AS VERBOSE CIPHER SYMBOLS:

python3.8 yablasto.py lat texts/examples/desine.lat.verbosebigr verbosebigr 400  2 > tmp/out.verbosebigr

UP TO 1/3 OF CIPHER CHARACTERS ARE NULLS:

python3.8 yablasto.py eng texts/examples/thesearethegenerations_long.eng.nulls nulls  400  2  > tmp/out.nulls

HOMOPHONIC CIPHER WHERE EACH PLAIN TEXT CHARACTER IS ENCODED AS A SYLLABLE/SHORT WORD (ONE TO MANY):

python3.8 yablasto.py eng texts/examples/thesearethegenerations_long.eng.syl syl 400 2  > tmp/out.syl

USE ITALIAN QUADGRAMS AND PLANET NAMES (U=V); UP TO 1/3 OF CIPHER CHARACTERS ARE NULLS:

python3.8 yablasto.py ita.uv texts/vms/f67r2_planets.eva.rev crib_planets_nulls 500 2

TODO:

Test crib without word spaces.

Fix example: eng texts/examples/thesearethegenerations_long.eng.verbosenulls verbosenulls 150 2

