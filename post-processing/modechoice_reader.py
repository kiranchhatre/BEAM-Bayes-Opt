#hange month-date in line 17

import os, glob, math, sys
import numpy as np
import pandas as pd
from tabulate import tabulate
 

Results_path = '/beam/output/sf-light'

dirs = next(os.walk(Results_path))[1]
subdirs = []
for x in dirs:
  a = os.path.join(Results_path,x)
  subdirs.append(a)

which_date = '03-09' # month-date
subdirs_i = []
for i in range(len(subdirs)):
  if which_date == subdirs[i][66:-13]:
    subdirs_i.append(subdirs[i]) 


mode_files = []
for y in subdirs_i:
  files = os.path.join(y,'referenceRealizedModeChoice.csv') 
  mode_files.append(files) 


conf_files = []
for i in range(len(mode_files)):
  if os.path.exists(mode_files[i]):
    files = mode_files[i][:-31]+'beam.conf' 
    conf_files.append(files)



params = ['time','last iteration','abs error sum','car', 'walk trans', 'drive_trans', 'ridehail trans', 'ridehail', 'ridehail pool', 'walk', 'bike']

err = []
a = []
diff_list = []
for i in range(len(mode_files)): 
  if os.path.exists(mode_files[i]):
    df = pd.read_csv(mode_files[i]).iloc[[0,-1]].drop(['iterations'],axis=1)
    acc = (df.iloc[0] - df.iloc[-1]).abs().sum()
    err.append(acc)
    directory = mode_files[i][:-32]+'/ITERS/'
    last_iter = max([os.path.join(directory,d) for d in os.listdir(directory)], key=os.path.getctime)
    last_iter_val = int(last_iter[94:])+1
    diff_list.append([mode_files[i][72:-36],last_iter_val,acc]) 

for i in range(len(conf_files)):
  with open(conf_files[i], 'r') as fin:
    file_text = fin.readlines()
  for i in range(25,33,1):
    file_text[i] = float(file_text[i].rpartition('=')[2]) 
    a.append(file_text[i])  

# time, last iter, error, params

n = 0
for i in range(len(diff_list)):
  diff_list[i].extend(a[n:n+8:])
  n = n + 8

print('\n'+subdirs[0][43:-29]+' 21 ITERS 8 Workers | Run @ '+ which_date +' | m5a.24xlarge'+'\n')

print(tabulate(diff_list,headers=params,tablefmt='orgtbl'))


print('\n')



print('Maximum abs error: ', max(err))
print('Minimum abs error: ', min(err)) 
improv = max(err) - min(err) 
print('Improvment in: ',improv ,'\n')
print('Info: 8 intercepts optimization at 0.0 value each reference simulation. [NEGLECT THIS LINE]\n')










