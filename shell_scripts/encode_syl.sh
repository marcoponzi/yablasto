# add 0 to each character; _ as syllable separator
sed -e 's/\([^ ]\)/\10 /g'  | sed -e 's/  */_/g' > tmp/out

cp tmp/out tmp/out1

for c in `grep -o . tmp/out | grep '[^_0]' | sort | uniq `
do
echo -n $c' '
grep -o $c tmp/out | wc -l
done | sort -rnk 2 | head -10 | grep -o '^.' > tmp/top_chars

#for c in `grep -o . tmp/out | grep '[^_]' | sort | uniq | head -11`
for c in `cat tmp/top_chars`
do
  #cat tmp/out1 | sed -e 's/\(0_.0_.0_.0_.0_.0_.0\)_'$c'0/\1_'$c'1/g' | sed -e 's/_$//' > tmp/out2
  cat tmp/out1 | sed -e 's/\('$c'0[^'$c']*\)_'$c'0/\1_'$c'1/g' | sed -e 's/_*$/_/' > tmp/out2
  mv tmp/out2 tmp/out1
done

cat tmp/out1
