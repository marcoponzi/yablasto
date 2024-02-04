tr '\n' ' ' > tmp/res.txt

patt='...............'
for c in 3 4 # nulls
do
cat tmp/res.txt | sed -e 's/\('$patt'\)/\1'$c'/g' > tmp/res1.txt
mv tmp/res1.txt tmp/res.txt
patt=$patt'.......................'
done

# 5 and 6 once (nulls)
cat tmp/res.txt | sed -e 's/\(...........\)/\16/'  | sed -e 's/\(..\)/\15/'> tmp/res1.txt
mv tmp/res1.txt tmp/res.txt

#for c in 5 6 # once
#do
#cat tmp/res.txt | sed -e 's/\('$patt'\)/\1'$c'/' > tmp/res1.txt
#mv tmp/res1.txt tmp/res.txt
#patt=$patt'...........'
#done

# h a
cat tmp/res.txt |\
sed -e 's/h/SO/g' |\
sed -e 's/a/22/g' |\
tr o  O |\
tr y  T |\
tr c  H |\
tr d  N |\
tr e  E |\
tr i  1 |\
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
tr b  Z | tr [:upper:] [:lower:] 
