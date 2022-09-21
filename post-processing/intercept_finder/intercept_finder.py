import numpy as np 
import pandas as pd 
import os, glob, shutil

where_at = 'OPTIMIZATION_ROOT/import_data/'
weights = np.zeros((8,8))
imported_data = sorted((next(os.walk(where_at))[1]))
Idx = [8, 1, 3, 5, 6, 4, 7, 2]

def intercept_reader(filepath):
    with open(filepath, 'r') as fin:
        file_text=fin.readlines()[24:32]
    for i in range(len(file_text)):
        file_text[i] = float(file_text[i].split('= ',1)[1:][0])
    file_text = [file_text[i] for i in Idx]
    return file_text

def modeshare_reader(filepath):
    df = pd.read_csv(filepath) 
    outputlist = df.loc[1].tolist()
    outputlist.remove(outputlist[0])
    return outputlist

def benchmark_reader(filepath):
    df = pd.read_csv(filepath) 
    outputlist = df.loc[0].tolist()
    outputlist.remove(outputlist[0])
    return outputlist

for i in range(len(imported_data)-1):
    this_iter_weights = np.zeros((8,8))
    modeshare_i, modeshare_next_i, intercept_i, intercept_next_i, delta_modeshare, delta_intercept = ([] for i in range(6))
    ms_filepaths = [where_at+imported_data[i]+'/ce.csv',where_at+imported_data[i+1]+'/ce.csv']
    ic_filepaths = [where_at+imported_data[i]+'/m.conf',where_at+imported_data[i+1]+'/m.conf']
    intercept_i, intercept_next_i = intercept_reader(ic_filepaths[0]), intercept_reader(ic_filepaths[1])
    modeshare_i, modeshare_next_i = modeshare_reader(ms_filepaths[0]), modeshare_reader(ms_filepaths[1])
    delta_modeshare = [x1 - x2 for (x1, x2) in zip(modeshare_i, modeshare_next_i)]
    delta_intercept = [x1 - x2 for (x1, x2) in zip(intercept_i, intercept_next_i)]
    
    '''
    # Only for Beamville
    del delta_modeshare[2:3]
    '''

    for i in range(len(delta_modeshare)):
        for j in range(len(delta_intercept)):
            this_iter_weights[i][j] = float(delta_modeshare[i]/delta_intercept[j])
    weights = (weights + this_iter_weights)/i

# Find required delta modeshares
benchmark = benchmark_reader(where_at+imported_data[-1]+'/ce.csv')

'''
# Only for Beamville
del benchmark[2:3]
'''

current_status = modeshare_reader(where_at+imported_data[-1]+'/ce.csv')

'''
# Only for Beamville
del current_status[2:3]
'''

req_delta_modeshare = [a_i - b_i for a_i, b_i in zip(benchmark, current_status)]
Approx_intercepts = np.linalg.inv(weights).dot(req_delta_modeshare)

Total_L1_distance = sum(list(map(abs, req_delta_modeshare)))
print(Total_L1_distance)
print(Approx_intercepts) 

