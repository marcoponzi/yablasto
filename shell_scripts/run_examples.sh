
RESTARTS=400

echo 
echo lat texts/examples/desine.lat.simple simplesub 50
time python3.6 yablasto.py lat texts/examples/desine.lat.simple simplesub 50  > tmp/out.simplesub
cat tmp/out.simplesub | tail -10

echo
echo eng texts/examples/thesearethegenerations_long.eng.syl syl $RESTARTS
time python3.6 yablasto.py eng texts/examples/thesearethegenerations_long.eng.syl syl $RESTARTS > tmp/out.syl
cat tmp/out.syl | tail -10

echo
echo eng eng texts/examples/thesearethegenerations_long.eng.nulls nulls $RESTARTS
time python3.6 yablasto.py eng texts/examples/thesearethegenerations_long.eng.nulls nulls  $RESTARTS  > tmp/out.nulls
cat tmp/out.nulls | tail -10

echo 
echo lat texts/examples/desine.lat.verbose verbosebigr $RESTARTS
time python3.6 yablasto.py lat texts/examples/desine.lat.verbose verbosebigr $RESTARTS > tmp/out.verbosebigr
cat tmp/out.verbosebigr | tail -10





