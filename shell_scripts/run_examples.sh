
RESTARTS=400


echo 
echo lat texts/examples/desine.lat.simple simplesub 100
time python3.6 yablasto.py lat texts/examples/desine.lat.simplesub simplesub 100  > tmp/out.simplesub
cat tmp/out.simplesub | tail -10

echo 
echo ita texts/examples/rottodaglianni.ita.simple simplesub 100
time python3.6 yablasto.py ita texts/examples/rottodaglianni.ita.simplesub simplesub 100  > tmp/out.ita.simplesub
cat tmp/out.simplesub | tail -10
echo
echo eng texts/examples/thesearethegenerations_long.eng.syl syl $RESTARTS
time python3.6 yablasto.py eng texts/examples/thesearethegenerations_long.eng.syl syl $RESTARTS > tmp/out.syl
cat tmp/out.syl | tail -10

echo
echo eng texts/examples/thesearethegenerations_long.eng.nulls nulls $RESTARTS
time python3.6 yablasto.py eng texts/examples/thesearethegenerations_long.eng.nulls nulls  $RESTARTS  > tmp/out.nulls
cat tmp/out.nulls | tail -10

echo 
echo eng.uv texts/examples/thesearethegenerations_long.eng.uv.verbosebigr verbosebigr $RESTARTS
time python3.6 yablasto.py eng.uv texts/examples/thesearethegenerations_long.eng.uv.verbosebigr verbosebigr $RESTARTS > tmp/out.verbosebigr
cat tmp/out.verbosebigr | tail -10





