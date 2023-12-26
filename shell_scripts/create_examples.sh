
for f in `ls -1 ../texts/examples/*.lat` `ls -1 ../texts/examples/*.eng` `ls -1 ../texts/examples/*.ita`
do
echo $f
cat $f | source encode_simplesub.sh > $f'.'simple
cat $f | tr u v > tmp/text.uv
cat tmp/text.uv | source encode_simplesub.sh  > $f'.uv.'simple
cat $f | source encode_verbose_sub.sh > $f'.'verbose
cat $f | source encode_nulls.sh > $f'.'nulls
cat $f | source encode_syl.sh > $f'.'syl
done
