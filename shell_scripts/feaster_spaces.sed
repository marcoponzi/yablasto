# see eva_encode.sed: 1-6 are gallows and benched-gallows
# https://griffonagedotcom.wordpress.com/2020/08/24/ruminations-on-the-voynich-manuscript/

# Before q
# After g, m, n
# After r except before y, i
# After s before ch (with or without inserted gallows), Sh, d, l 
# After y except before t, k
# After l before r, o, d, ch (with or without inserted gallows), Sh
# Between repetitions of o, s, l

s/q/ q/g
s/\([gmn]\)/\1 /g
s/r\([^iy]\)/r \1/g
s/s\([1-6dl]\)/s \1/g
s/y\([^tk]\)/y \1/g
s/l\([rod1-6]\)/l \1/g
###s/lS/l S/g
s/\([osl]\)\1/\1 \1/g
s/  */ /g
