from astropy.table import Table as t
import os
from gammacat.utils import load_yaml

rootdir = './input/data'
sourcedir = './input/sources'
source_def_refs = dict()
gammacat_yaml_refs = dict()
gammacat_ecsv_refs = dict()
filenames = ['empty']
source_def_files = ['empty']

# Filling list filenames with all fil pathes in ./input/data
for root, dirs, files in os.walk(rootdir, topdown=False):
    for name in files:
        filepath = os.path.join(root,name)
        filenames.append(filepath)
filenames.pop(0)

# Filling list source_def_files with all file pathes in ./input/sources
for root, dirs, files in os.walk(sourcedir, topdown=False):
    for name in files:
        source_def_files.append(os.path.join(root,name))
source_def_files.pop(0)

# Filling dictionaries
for source_def_file in source_def_files:
    if(source_def_file[len(source_def_file)-4:len(source_def_file)] == 'yaml'):
        data = load_yaml(source_def_file)
        # Filling dictionary source_def_refs with info from files in ./input/sources; [source_id, reference_ids]
        source_def_refs[data['source_id']] = data['reference_ids']
        # Filling dictionaries gammacat_*_refs with source_id as keys
        gammacat_yaml_refs[data['source_id']] = []
        gammacat_ecsv_refs[data['source_id']] = []

for file in filenames:
    # Filling dictionary gammacat_yaml_refs with reference_id from yaml-files in ./input/data
    if(file[len(file)-4:len(file)] == 'yaml'):
        yaml_data = load_yaml(file)
        print(yaml_data['source_id'])
        gammacat_yaml_refs[yaml_data['source_id']].append(yaml_data['reference_id'])
    # Filling dictionary gammacat_ecsv_refs with reference_id from ecsv-files in ./input/data
    elif(file[len(file)-4:len(file)] == 'ecsv'):
        ecsv_data = t.read(file, format='ascii.ecsv', delimiter=' ')
        gammacat_ecsv_refs[ecsv_data.meta['source_id']].append(ecsv_data.meta['reference_id'])

# Check for consistency between reference_ids in ./input/sources/*.yaml and the files in ./input/data
for key in source_def_refs:
    for reference in source_def_refs[key]:
        if(reference not in gammacat_yaml_refs[key]):
            print('WARNING: Missing yaml file for source {}, reference {}'.format(key, reference))
        if(reference not in gammacat_ecsv_refs[key]):
            print('WARNING: Missing ecsv file for source {}, reference {}'.format(key, reference))
        else:
            continue