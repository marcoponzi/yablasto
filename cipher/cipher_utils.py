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
  
def load_crib(fname):
    words=list()
    with open("texts/examples/"+fname, "r") as infile:
        for line in infile:
            w = line.split("\n")[0]
            words.append( w.upper() )
    return sorted(sorted(words), key=len, reverse=True)
