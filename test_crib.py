import cipher.crib as crib
import cipher.simplesub as simplesub
import cipher.cipher_utils as cipher_utils

cipher_utils.set_my_log(True)

crib.set_module(simplesub, 'constellations', 'lat')

score=crib.score(-10,"NULLUS CANIS MINOR")
print(score)
print()
score=crib.score(-10,"NULLUS CANIS MINNOR")
print(score)
print()
score=crib.score(-10,"NULLUS ADROMEDA CARCER LEO ARS XX")
print(score)
print()
score=crib.score(-10,"FASSFDSARECCRWDAFAEFFFASEE CANIS ARAW")
print(score)
print()
score=crib.score(-10,"FASSFDSARECCRWDAFAEFFFASEE FDAFW REWD")
print(score)
print()
score=crib.score(-10,"FASSFDSARECCRWDAFAEFFFASEEPPREWD")
print(score)
print()
score=crib.score(-10,"FASSFDSARIECRWDAFAETAURUSEEPPREWD")
print(score)

mylist=('a','b','c')
for i in range(0,9):
  print(cipher_utils.frequency_choice(mylist))
