source encode_simple_sub.sh > tmp/simple
PATT='.....'
#for c in 2 3 4 5 6 7 8 9 - % # @ i a
for c in 2 3 4 #5 6 7 8 9 - % # @ i a
do
cat tmp/simple | sed -e 's/\('$PATT'\)/\1'$c'/g' > tmp/out
mv tmp/out tmp/simple
PATT=$PATT'.....'
done

cat tmp/simple
