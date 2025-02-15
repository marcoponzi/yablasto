
for lang in lat eng ita deu
do
for f1 in `ls -1 ../texts/examples/*'.'$lang` `ls -1 ../texts/cribs/*'.'$lang` 
do
  echo $f1

  cat $f1 | tr u v > $f1'.uv' # u and v equivalent

  for f in $f1 $f1'.uv'
  do
  cat $f | source encode_anagr.sh > $f'.'anagr # anagrammed
  cat $f | sed -e 's/\(.\)\1/\1/g' > $f'.no2'  # remove doubles
  done
done
done

for f1 in `ls -1 ../texts/examples/*.lat` `ls -1 ../texts/examples/*.eng` `ls -1 ../texts/examples/*.ita`
do
echo $f1

for f in $f1 $f1'.uv'
do
cat $f | source encode_simplesub.sh > $f'.'simplesub
cat $f | source encode_simplesubanagr.sh > $f'.'simplesubanagr
cat $f | source encode_verbosebigr.sh > $f'.'verbosebigr
cat $f | source encode_verbosenulls.sh > $f'.'verbosenulls
cat $f | source encode_nulls.sh > $f'.'nulls
cat $f | source encode_syl.sh > $f'.'syl
done
done
