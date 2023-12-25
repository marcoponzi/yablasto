import re


    
# longer keys first
def sort_dict(indict):
  new_d = {}
  klist=list(indict.keys())
  klist=sorted(klist) #alphabetical
  klist=sorted(klist, key=len, reverse=True) #longer first

  for k in klist:
    new_d[k] = indict[k]

  return new_d
