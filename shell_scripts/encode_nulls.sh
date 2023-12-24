source encode_simplesub.sh > tmp/simple
cp tmp/simple tmp/nulls
PATT='.....'
# 2 3 4 as nulls
for c in 2 3 4 
do
cat tmp/nulls | sed -e 's/\('$PATT'\)/\1'$c'/g' > tmp/out
mv tmp/out tmp/nulls
PATT=$PATT'.....'
done

# 5, 6 as nulls - one occurrence each
cat tmp/nulls | sed -e 's/^\(......................\)/\15/' | sed -e 's/\(5..............\)/\16/' > tmp/out
mv tmp/out tmp/nulls

cat tmp/nulls
