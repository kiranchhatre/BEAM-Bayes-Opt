
import codecs, json
import numpy as np
import matplotlib.pyplot as plt

data=[]

path = 'OPTIMIZER ROOT PATH'

with codecs.open(path+'/results.json','rU','utf-8') as data_file:
  for line in data_file:
    data.append(json.loads(line))


for i in range(len(data)):
  del data[i][1:3]
  del data[i][-1] 

b = [x for x in data if x[1] is not None]

for i in range(len(b)):
  b[i].append(b[i][1]['loss'])
  del b[i][1]

absErr = []
xticks = []

for i in range(len(b)):
  absErr.append(b[i][1])
  #xticks.append(b[i][0]) 

x = np.array(list(range(len(b))))
#plt.xticks(x,xticks)
plt.plot(x,absErr)
plt.savefig('absErr.png')

