RESTARTS=90

for lang in ita lat ita.uv lat.uv
do
for fname in f67r2_red f67r2_black f67r2_12paragraphs
do
f=texts/vms/$fname

for crib in crib_zodiac crib_months
do
  for encoding in cuva bg cuva.rev bg.rev
  do
  for method in simplesub nulls verbosebigr verbosenulls
  do
  OUT=out'_'$fname'_'$lang'_'$encoding'_'$crib'_'$method
  echo; echo tmp/$OUT
  python3.6 yablasto.py $lang $f'.'$encoding $crib'_'$method $RESTARTS 1 > tmp/$OUT
  tail -10 tmp/$OUT
  done
  done

  
  method=syl
  for encoding in syl syl.rev
  do
  OUT=out'_'$fname'_'$lang'_'$encoding'_'$crib'_'$method
  echo; echo tmp/$OUT
  python3.6 yablasto.py $lang $f'.'$encoding $crib'_'$method $RESTARTS 1 > tmp/$OUT
  tail -10 tmp/$OUT
  done
done


done
done
