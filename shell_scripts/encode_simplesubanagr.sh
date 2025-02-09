tr a  X |\
tr e  Y |\
tr x  A |\
tr y  E |
sed -e 's/\([^ ,]\)\([^ ,]\)/\2\1/g' | tr ' ' ',' |  tr [:upper:] [:lower:]
