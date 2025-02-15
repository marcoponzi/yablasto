# unknown characters a -; remove <...> tags; single spaces; skip empty lines
sed -e 's/@[0-9][0-9]*;/-/g' | sed -e 's/<[^>]*>//g' | tr '?' '-' | sed -e 's/[^a-z -]//g' | \
  sed -e 's/^ *//g' | sed -e 's/  */ /g' |grep '[a-z]'
