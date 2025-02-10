
for f1 in `ls -1 ../texts/examples/*.lat` `ls -1 ../texts/examples/*.eng` `ls -1 ../texts/examples/*.ita`
do
echo $f1

cat $f1 | tr u v > $f1'.uv'

for f in $f1 $f1'.uv'
do
cat $f | source encode_simplesub.sh > $f'.'simplesub
cat $f | source encode_simplesubanagr.sh > $f'.'simplesubanagr
cat $f | source encode_anagr.sh > $f'.'anagr
cat $f | sed -e 's/\(.\)\1/\1/g' > $f'.no2'
cat $f | source encode_verbosebigr.sh > $f'.'verbosebigr
cat $f | source encode_verbosenulls.sh > $f'.'verbosenulls
cat $f | source encode_nulls.sh > $f'.'nulls
cat $f | source encode_syl.sh > $f'.'syl
done
done
