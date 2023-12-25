#s/y\([^ ]\)/y \1/g
s/[ay]/o/g
s/o\([^lirgsm ]\)/o \1/g
s/o\([^ ]\)o/o \1o/g
s/[ei]//g
#sh == ch
s/2/1/g
s/  */ /g
