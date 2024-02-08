RESTARTS=200

for lang in ita.uv lat.uv #ita lat 
do
for fname in f67r2_planets
do
  f=texts/vms/$fname

  crib=crib_planets
  for encoding in cuva bg eva gheuens cuva.rev bg.rev eva.rev gheuens.rev
  do
  for method in simplesub nulls verbosebigr
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
