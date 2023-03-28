#all "circles" are the same
s/[ay]/o/g
# space after each circle except the last one
# repeated to handle  overlap
s/o\([^ o]*o\)/o \1/g
s/o\([^ o]*o\)/o \1/g
# remove e,i
s/[7890ei]//g
#sh == ch
s/2/1/g
s/  */ /g
# space as line separator
s/ *$/ /
s/^ //
