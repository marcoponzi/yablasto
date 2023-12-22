# yablasto
# lower case plain text converted to upper case cipher
cat slowbrowncat.eng | source encode_simple_sub.sh > slowbrowncat.eng.cipher
cat flectere.lat  | source encode_simple_sub.sh > flectere.lat.cipher


COMPUTE SCORE OF PLAIN TEXT:
time python3.6 myblasto005.py lat texts/examples/flectere.lat.upper score 999

time python3.6 myblasto005.py lat texts/examples/desine.lat.verbose verbosebigr 300

time python3.6 myblasto005.py lat.uv texts/examples/desine.lat.uv.simple simplesub 50

time python3.6 myblasto005.py eng texts/examples/letthewaters.eng.verbose verbosebigr 300

time python3.6 myblasto005.py eng texts/examples/letthewaters.eng.nulls nulls 300

time python3.6 myblasto006.py eng texts/examples/thesearethegenerations_long.eng.syl syl 200

