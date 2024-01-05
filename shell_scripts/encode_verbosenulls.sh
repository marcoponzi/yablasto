sed -e 's/o/SE/g' |\
sed -e 's/e/ST/g' |\
tr h  1 |\
tr y  O |\
tr a  0 |\
tr c  H |\
tr d  N |\
sed -e 's/i/SS/g' |\
tr k  R |\
tr l  D |\
tr r  L |\
tr s  U |\
tr t  W |\
tr n  G |\
tr q  C |\
tr p  Y |\
tr m  M |\
tr f  F |\
tr g  P |\
tr x  B |\
tr v  K |\
tr z  V |\
tr w  Q |\
tr u  J |\
tr j  X |\
tr b  Z  | tr [:upper:] [:lower:] | tr '\n' ' ' > tmp/res.txt

patt='...............'
for c in 2 3 
do
cat tmp/res.txt | sed -e 's/\('$patt'\)/\1'$c'/g' > tmp/res1.txt
mv tmp/res1.txt tmp/res.txt
patt=$patt'..........'
done

for c in 4 5 6 # once
do
cat tmp/res.txt | sed -e 's/\('$patt'\)/\1'$c'/' > tmp/res1.txt
mv tmp/res1.txt tmp/res.txt
patt=$patt'.......'
done

cat tmp/res.txt
