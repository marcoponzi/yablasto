mkdir tmp
SHORT=150
LONG=300  


echo 
echo lat texts/examples/desine.lat.simple simplesub $SHORT 1.5 
python3.8 yablasto.py lat texts/examples/desine.lat simplesub score  | tail -1
time python3.8 yablasto.py lat texts/examples/desine.lat.simplesub simplesub $SHORT 1.5  > tmp/out.simplesub
cat tmp/out.simplesub | tail -10

echo 
echo ita texts/examples/rottodaglianni.ita.simple simplesub $SHORT 1.5 
python3.8 yablasto.py ita texts/examples/rottodaglianni.ita simplesub score | tail -1
time python3.8 yablasto.py ita texts/examples/rottodaglianni.ita.simplesub simplesub $SHORT 1.5  > tmp/out.ita.simplesub
cat tmp/out.ita.simplesub | tail -10

echo
echo eng texts/examples/thesearethegenerations_long.eng.syl syl $LONG 1.5 
python3.8 yablasto.py eng texts/examples/thesearethegenerations_long.eng syl score | tail -1
time python3.8 yablasto.py eng texts/examples/thesearethegenerations_long.eng.syl syl $LONG 1.5 > tmp/out.syl
cat tmp/out.syl | tail -10

echo
echo eng texts/examples/thesearethegenerations_long.eng.nulls nulls $LONG 1.5 
python3.8 yablasto.py eng texts/examples/thesearethegenerations_long.eng nulls score | tail -1
time python3.8 yablasto.py eng texts/examples/thesearethegenerations_long.eng.nulls nulls  $LONG 1.5  > tmp/out.nulls
cat tmp/out.nulls | tail -10

echo 
echo eng.uv texts/examples/thesearethegenerations_long.eng.uv.verbosebigr verbosebigr $LONG 0.05 
python3.8 yablasto.py eng.uv texts/examples/thesearethegenerations_long.eng.uv verbosebigr score | tail -1
time python3.8 yablasto.py eng.uv texts/examples/thesearethegenerations_long.eng.uv.verbosebigr verbosebigr $LONG 0.05 >\
     tmp/out.verbosebigr
cat tmp/out.verbosebigr | tail -10

echo
echo eng texts/examples/thesearethegenerations_long.eng.verbosenulls verbosenulls $SHORT 2
python3.8 yablasto.py eng texts/examples/thesearethegenerations_long.eng verbosenulls score | tail -1
time python3.8 yablasto.py eng texts/examples/thesearethegenerations_long.eng.verbosenulls verbosenulls $SHORT 2  >\
	     tmp/out.verbosenulls
cat tmp/out.verbosenulls | tail -10

echo
echo lat.anagr texts/examples/enim.manet.lat.simplesubanagr simplesubanagr $SHORT 7
python3.8 yablasto.py lat.anagr texts/examples/enim.manet.lat simplesubanagr score | tail -1
time python3.8 yablasto.py lat.anagr texts/examples/enim.manet.lat.simplesubanagr simplesubanagr $SHORT 7 >\
	     tmp/out.enim.simplesubanagr
cat tmp/out.enim.simplesubanagr | tail -10

echo
echo lat.anagr texts/examples/desine.lat.simplesubanagr simplesubanagr $SHORT 7
python3.8 yablasto.py lat.anagr texts/examples/desine.lat.simplesubanagr simplesubanagr score | tail -1
time python3.8 yablasto.py lat.anagr texts/examples/desine.lat.simplesubanagr simplesubanagr $SHORT 7 >\
	     tmp/out.desine.simplesubanagr
cat tmp/out.desine.simplesubanagr | tail -10

echo
echo lat.anagr texts/examples/primum_aries.lat.simplesubanagr crib_constellations_simplesubanagr  $LONG 21
time python3.8 yablasto.py lat.anagr texts/examples/primum_aries.lat.simplesubanagr crib_constellations_simplesubanagr  $LONG 21  >\
             tmp/out.primum_aries.lat.simplesubanagr
cat tmp/out.primum_aries.lat.simplesubanagr | tail -10

