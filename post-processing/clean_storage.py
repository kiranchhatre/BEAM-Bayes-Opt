
dir = 'OUTPUT PATH'
import os

for parent, dirnames, filenames in os.walk(dir):
  for fn in filenames:
    if fn.lower().endswith('.gz'):
      os.remove(os.path.join(parent,fn))










