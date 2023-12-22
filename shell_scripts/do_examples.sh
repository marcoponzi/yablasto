
for f in `ls -1 ../texts/examples/*.lat` `ls -1 ../texts/examples/*.eng`
do
echo $f
cat $f | source encode_simple_sub.sh > $f'.'simple
cat $f | tr u v > tmp/text.uv
cat tmp/text.uv | source encode_simple_sub.sh  > $f'.uv.'simple
cat $f | source encode_verbose_sub.sh > $f'.'verbose
cat $f | source encode_simplesub_with_nulls.sh > $f'.'nulls
cat $f | source encode_syl.sh > $f'.'syl
done
