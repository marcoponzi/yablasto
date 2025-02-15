IVTTDIR=~/rec/voynich/software/ivtt
BITRANSDIR=~/rec/voynich/software/bitrans

# a0=keep @nnn; codes (rare characters)
# c4=remove comments
# h1=keep uncertain spaces; h2=ignore uncertain spaces
# s1=blank for spaces
# u1=pick first uncertain reading
# -@L=no Labels; +@L labels only
# f0=keep foliation information
# <! page header (removed)


for p in f68r1 f68r2 f68r3 
do
$IVTTDIR/ivtt $IVTTDIR/ZL_ivtff_2b.txt -a0 -c4 -h1 -s1 +@L -u1 -f0 | grep $p |\
 source ./clean_ivtt.sh > ../texts/vms/$p'.eva'
done

cat ../texts/vms/f68r[12].eva > ../texts/vms/f68r_1_2.eva

for p in f3r f34v 
do
$IVTTDIR/ivtt $IVTTDIR/ZL_ivtff_2b.txt -a0 -c4 -h1 -s1 -u1 -f0 | grep $p |\
 source ./clean_ivtt.sh > ../texts/vms/$p'.eva'
done

# zodiac / month labels: spaces removed to make sets of 12 words
$IVTTDIR/ivtt $IVTTDIR/ZL_ivtff_2b.txt -a0 -c4 -h1 -s1 +@L -u1 -f0 | grep f67r2 |\
  grep -v '<!' | head -12  | source ./clean_ivtt.sh  > ../texts/vms/f67r2_12red_sp.eva
$IVTTDIR/ivtt $IVTTDIR/ZL_ivtff_2b.txt -a0 -c4 -h1 -s1 +@L -u1 -f0 | grep f67r2 |\
  grep 'Ls' | source ./clean_ivtt.sh  > ../texts/vms/f67r2_12inner_sp.eva
  
cat ../texts/vms/f67r2_12red_sp.eva | tr -d ' ' > ../texts/vms/f67r2_12red_nosp.eva
cat ../texts/vms/f67r2_12inner_sp.eva | tr -d ' ' > ../texts/vms/f67r2_12inner_nosp.eva

$IVTTDIR/ivtt $IVTTDIR/ZL_ivtff_2b.txt -a0 -c4 -h1 -s1 -u1 -@L -f0 | grep f67r2 | grep 'Pb'|\
 source ./clean_ivtt.sh  > ../texts/vms/f67r2_12paragraphs.eva
 
for p in f3r f34v f68r3 f67r2_12paragraphs f67r2_planets f67r2_12inner_sp f67r2_12red_sp f67r2_12inner_nosp f67r2_12red_nosp \
  f68r1 f68r2 f68r_1_2
do
$BITRANSDIR/bitrans -f $BITRANSDIR/Eva-Cuva.bit ../texts/vms/$p'.eva' ../texts/vms/$p'.cuva'
cat ../texts/vms/$p'.cuva' | tr [:upper:] [:lower:] | sed -e 's/[^a-z -]//g' > temp.cuva
mv temp.cuva  ../texts/vms/$p'.cuva'
cat ../texts/vms/$p'.eva' | sed -f eva_bench_gallows.sed > ../texts/vms/$p'.bg' # bench and gallows replaced
cat ../texts/vms/$p'.bg'| tr -d ' ' | sed -f feaster_spaces.sed > ../texts/vms/$p'.feaster'
cat ../texts/vms/$p'.eva' | sed -f gheuens_verbose.sed > ../texts/vms/$p'.gheuens'
cat ../texts/vms/$p'.feaster' | sed -f more_spaces.sed | tr ' ' '_' > ../texts/vms/$p'.syl'
done

for f in ../texts/vms/f68r3* # merge labels as single words
do
  cat $f | tr -d ' ' > temp.f68r3
  mv temp.f68r3 $f
done

for f in ../texts/vms/*eva ../texts/vms/*cuva ../texts/vms/*bg ../texts/vms/*gheuens ../texts/vms/*syl
do
cat $f | tr '\n' '#' | grep -o . | tac | tr -d '\n' | tr '#' '\n' > $f'.rev'
done



