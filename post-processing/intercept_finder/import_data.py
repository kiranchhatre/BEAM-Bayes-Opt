import os, glob, shutil

data = 'BEAM_ROOT/beam/output/beamville/'
all_results = next(os.walk(data))[1]
where_to = 'OPTIMIZATION_ROOT/import_data'
types = ('beam.conf', 'referenceRealizedModeChoice.csv')

if os.path.exists(where_to):
    shutil.rmtree(where_to)
os.makedirs(where_to)

for i in range(len(all_results)):
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(data+all_results[i]+'/'+files))
    temp_folder=where_to+'/'+all_results[i][-18:-4]
    if os.path.exists(temp_folder):
        temp_folder = where_to+'/'+all_results[i][-18:-5]+str(int(all_results[i][-5:-4])+1)
        os.makedirs(temp_folder) 
    else:
        os.makedirs(temp_folder)
    for j in range(len(files_grabbed)):
        shutil.copyfile(files_grabbed[j], temp_folder+'/'+files_grabbed[j][-6:])   



