IVTTDIR=~/rec/voynich/software/ivtt
BITRANSDIR=~/rec/voynich/software/bitrans

rm ../texts/vms/*

# a0=keep @nnn; codes (rare characters)
# c4=remove comments
# h1=keep uncertain spaces; h2=ignore uncertain spaces
# s1=blank for spaces
# u1=pick first uncertain reading
# -@L=no Labels
# f0=keep foliation information
# <! page header (removed)

for p in f3r f34v
do
$IVTTDIR/ivtt $IVTTDIR/ZL_ivtff_2b.txt -a0 -c4 -h1 -s1 -u1 -@L -f0 | grep $p |\
 sed -e 's/@[0-9][0-9]*;/-/g' | sed -e 's/<[^>]*>//g' | tr '?' '-' | sed -e 's/[^a-z -]//g' | sed -e 's/  */ /g' |\
 grep '[a-z]'> ../texts/vms/$p'.eva'
 
$BITRANSDIR/bitrans -f $BITRANSDIR/Eva-Cuva.bit ../texts/vms/$p'.eva' ../texts/vms/$p'.cuva'
cat ../texts/vms/$p'.cuva' | tr [:upper:] [:lower:] > temp.cuva
mv temp.cuva  ../texts/vms/$p'.cuva'
cat ../texts/vms/$p'.eva' | sed -f eva_bench_gallows.sed > ../texts/vms/$p'.bg' # bench and gallows replaced
cat ../texts/vms/$p'.bg'| tr -d ' ' | sed -f feaster_spaces.sed > ../texts/vms/$p'.feaster'
cat ../texts/vms/$p'.feaster' | sed -f more_spaces.sed | tr ' ' '_' > ../texts/vms/$p'.syl'
done
