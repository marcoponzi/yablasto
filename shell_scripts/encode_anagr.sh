tr ' ' ',' | cat > tmp_in.file
for w in `cat tmp_in.file | tr ',' '\n'`
do
echo $w | grep -o . | sort | tr -d '\n'
echo
done
rm tmp_in.file
