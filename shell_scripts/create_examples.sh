
for f in `ls -1 ../texts/examples/*.lat` `ls -1 ../texts/examples/*.eng` `ls -1 ../texts/examples/*.ita`
do
echo $f
cat $f | source encode_simplesub.sh > $f'.'simplesub
cat $f | tr u v > $f'.uv'
cat $f | sed -e 's/\(.\)\1/\1/g' > $f'.no2'
cat $f'.no2'  | tr u v > $f'.no2.uv'
cat $f'.uv' | source encode_simplesub.sh  > $f'.uv.'simplesub
cat $f | source encode_verbosebigr.sh > $f'.'verbosebigr
cat $f'.uv' | source encode_verbosebigr.sh > $f'.uv.'verbosebigr
cat $f | source encode_nulls.sh > $f'.'nulls
cat $f | source encode_syl.sh > $f'.'syl
done
