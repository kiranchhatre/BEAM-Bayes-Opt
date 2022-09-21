
import codecs, json, collections
from operator import itemgetter
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

json_file = 'RESULT LOG DIR PATH/results.json'
data = []

with codecs.open(json_file, 'rU', 'utf-8') as data_file:
    for line in data_file:
        data.append(json.loads(line))

for i in range(len(data)):
    del data[i][1:3]
    del data[i][-1]

b = [x for x in data if x[1] is not None]

for u in range(len(b)):
    b[u].append(b[u][1]['loss'])
    del b[u][1]

w1, w2, w3, w4 = ([] for i in range(4))

for i in range(len(b)):
    if b[i][0][2] == 0:
        w1.append(b[i])
        w1 = sorted(w1, key=itemgetter(0))
    elif b[i][0][2] == 1:
        w2.append(b[i])
        w2 = sorted(w2, key=itemgetter(0))
    elif b[i][0][2] == 2:
        w3.append(b[i])
        w3 = sorted(w3, key=itemgetter(0))
    elif b[i][0][2] == 3:
        w4.append(b[i])
        w4 = sorted(w4, key=itemgetter(0))


for u in range(len(w1)):
    w1[u].append(w1[u][0][0])
    del w1[u][0]

for v in range(len(w2)):
    w2[v].append(w2[v][0][0])
    del w2[v][0]
    
for w in range(len(w3)):
    w3[w].append(w3[w][0][0])
    del w3[w][0]

for x in range(len(w4)):
    w4[x].append(w4[x][0][0])
    del w4[x][0]


#create line joining lowermost points

absE1, absE2, absE3, absE4, x1, x2, x3, x4, res_err, res_x  = ([] for i in range(10))

for i in range(len(w1)):
  absE1.append(w1[i][0])
  x1.append(w1[i][1])
for i in range(len(w2)):
  absE2.append(w2[i][0])
  x2.append(w2[i][1])
for i in range(len(w3)):
  absE3.append(w3[i][0])
  x3.append(w3[i][1])
for i in range(len(w4)):
  absE4.append(w4[i][0])
  x4.append(w4[i][1])

all_x = x1 + x2 + x3 + x4
all_absE = absE1 + absE2 + absE3 + absE4
total = [[i,j] for i,j in zip(all_x,all_absE)]
# additional TEMPORARY LINE!!!
total.append([1,160])
total = sorted(total, key=itemgetter(0))

all_iters = list(range(0,total[-1][0]+1,1))
lowest_errs = []

for i in range(len(all_iters)): 
    a = [all_iters[i]]
    b = [element for element in total if element[0] in a]
    lowest_errs.append(min(b))

least_so_far = lowest_errs[0][1] 
result = []
for x in lowest_errs:
    if x[1] <= least_so_far: 
        result.append(x)
        least_so_far = x[1]
for i in range(len(result)):
  res_err.append(result[i][1])
  res_x.append(result[i][0])

res_err.append(res_err[-1])
res_x.append(total[-1][0]) 

# Plotting

fig, ax = plt.subplots()
for color in ['tab:blue']:
    ax.scatter(all_x, all_absE, c=color,
               alpha=0.4, edgecolors='none', label='Trial loss')
ax.set_xlim(xmin=0)
ax.set_xlim(xmax=total[-1][0])
 
plt.step(res_x, res_err, where='post', linestyle='--', color='red', linewidth=0.5, label='Model progress')
plt.legend(title='Optimization at:')

plt.xlabel("Trial Number")
plt.ylabel("L1-norm")
plt.title("Urbansim-10k-optimization") 
plt.savefig('Urbansim-10k-optimization')











