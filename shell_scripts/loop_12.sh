
for crib in zodiac months
do

for translit in bg cuva eva gheuens
do
for lang in deu ita lat
do
for vms in f67r2_12red_sp f67r2_12red_nosp f67r2_12inner_sp f67r2_12inner_nosp
do

echo
echo $lang'.uv.anagr' texts/vms'/'$vms'.'$translit crib'_'$crib'_'simplesubanagr
time python3.8 yablasto.py $lang'.uv.anagr' texts/vms'/'$vms'.'$translit crib'_'$crib'_'simplesubanagr 100 21  >\
             tmp/14_loop_out_$lang'_'$vms'.'$translit'_'$crib'.txt'  2>&1
tail -10 tmp/14_loop_out_$lang'_'$vms'.'$translit'_'$crib'.txt'

done
done
done
done
