RESTARTS=300

for f in texts/vms/f34v.eva  texts/vms/f3r.eva
do
root=`echo $f | sed -e 's/.eva//'`
folio=`echo $root | sed -e 's%.*/%%'`

for lang in ita.uv lat.uv eng
do
  
  for encoding in cuva bg
  do
  for method in simplesub nulls verbosebigr
  do
  echo; echo tmp/out'.'$folio'.'$lang'.'$encoding'.'$method
  python3.6 yablasto.py $lang $root'.'$encoding $method $RESTARTS > tmp/out'_'$folio'_'$lang'_'$encoding'_'$method
  done
  done
encoding=syl
method=syl
echo; echo tmp/out'.'$folio'.'$lang'.'$encoding'.'$method
python3.6 yablasto.py $lang $root'.'$encoding $method $RESTARTS > tmp/out'_'$folio'_'$lang'_'$encoding'_'$method

done

done
